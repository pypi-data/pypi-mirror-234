import os
import sys
import logging
import subprocess
import boto3
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import pytz
import io
from tqdm import tqdm

from SharedData.Logger import Logger
from SharedData.MultiProc import io_bound_process


def S3GetSession(isupload=False):
    _session = boto3.Session(profile_name=os.environ['S3_AWS_PROFILE'])
    if 'S3_ENDPOINT_URL' in os.environ:
        _s3 = _session.resource(
            's3', endpoint_url=os.environ['S3_ENDPOINT_URL'])
    else:
        _s3 = _session.resource('s3')
    _bucket = _s3.Bucket(os.environ['S3_BUCKET'].replace('s3://', ''))
    return _s3, _bucket


def S3ListFolder(prefix):
    s3, bucket = S3GetSession()
    keys = np.array(
        [obj_s.key for obj_s in bucket.objects.filter(Prefix=prefix)])
    return keys


def S3Download(remote_path, local_path=None, \
        force_download=False, local_mtime=None):
    bucket_name = os.environ['S3_BUCKET'].replace('s3://', '')
    s3_path = str(remote_path).replace(
        os.environ['DATABASE_FOLDER'], '').replace('\\', '/')[1:]
    s3, bucket = S3GetSession()
    # load obj
    obj = s3.Object(bucket_name, s3_path)
    remote_mtime = None
    try:
        # remote mtime
        remote_mtime = obj.last_modified.timestamp()
        if 'mtime' in obj.metadata:
            remote_mtime = float(obj.metadata['mtime'])
        remote_exists = True
    except:
        # remote file dont exist
        remote_exists = False

    local_exists = False
    if not local_path is None:
        remote_isnewer = False
        local_exists = os.path.isfile(str(local_path))
        local_mtime = None
        if local_exists:
            # local mtime
            local_mtime = datetime.utcfromtimestamp(
                os.path.getmtime(local_path)).timestamp()
    elif not local_mtime is None:
        local_mtime = datetime.utcfromtimestamp(local_mtime).timestamp()
        local_exists = True

    remote_isnewer = False
    if (local_exists) & (remote_exists):
        # compare
        remote_isnewer = remote_mtime > local_mtime

    if remote_exists:
        if (not local_exists) | (remote_isnewer) | (force_download):
            # get object size for progress bar
            obj_size = obj.content_length / (1024*1024)  # in MB
            description = 'Downloading:%iMB, %s' % (obj_size, s3_path)
            io_obj = io.BytesIO()
            try:
                if obj_size > 50:
                    with tqdm(total=obj_size, unit='MB', unit_scale=True,\
                               desc=description) as pbar:
                        obj.download_fileobj(io_obj,
                            Callback=lambda bytes_transferred: \
                                pbar.update(bytes_transferred/(1024*1024)))
                else:
                    obj.download_fileobj(io_obj)
                return [io_obj, local_mtime, remote_mtime]
            except Exception as e:
                raise Exception('downloading %s,%s ERROR!\n%s' %
                                (Logger.user, remote_path, str(e)))

    return [None, local_mtime, remote_mtime]


def UpdateModTime(local_path, remote_mtime):
    # update modification time
    remote_mtime_dt = datetime.fromtimestamp(remote_mtime)
    offset = remote_mtime_dt - datetime.utcfromtimestamp(remote_mtime)
    remote_mtime_local_tz = remote_mtime_dt+offset
    remote_mtime_local_tz_ts = remote_mtime_local_tz.timestamp()
    os.utime(local_path, (remote_mtime_local_tz_ts, remote_mtime_local_tz_ts))


def S3SaveLocal(local_path, io_obj, remote_mtime):
    path = Path(local_path)
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    with open(local_path, 'wb') as f:
        f.write(io_obj.getbuffer())
        f.flush()
    # update modification time
    remote_mtime_dt = datetime.fromtimestamp(remote_mtime)
    offset = remote_mtime_dt - datetime.utcfromtimestamp(remote_mtime)
    remote_mtime_local_tz = remote_mtime_dt+offset
    remote_mtime_local_tz_ts = remote_mtime_local_tz.timestamp()
    os.utime(local_path, (remote_mtime_local_tz_ts, remote_mtime_local_tz_ts))


def S3Upload(file_io, path, mtime):
    remotefilepath = str(path).replace(
        os.environ['DATABASE_FOLDER'], os.environ['S3_BUCKET'])
    remotefilepath = remotefilepath.replace('\\', '/')

    # Check the file size
    file_size = file_io.seek(0, os.SEEK_END) / (1024*1024)  # in MB
    file_name = remotefilepath.replace(os.environ['S3_BUCKET'], '')[1:]
    description = 'Uploading:%iMB, %s' % (file_size, file_name)

    trials = 3
    success = False
    file_io.close = lambda: None  # prevents boto3 from closing io
    while trials > 0:
        try:
            s3, bucket = S3GetSession(isupload=True)
            mtime_utc = datetime.utcfromtimestamp(mtime).timestamp()
            mtime_str = str(mtime_utc)

            file_io.seek(0)
            if file_size > 50:
                with tqdm(total=file_size, unit='MB', unit_scale=True, desc=description) as pbar:
                    bucket.upload_fileobj(file_io, file_name,
                                          ExtraArgs={'Metadata': {
                                              'mtime': mtime_str}},
                                          Callback=lambda bytes_transferred: pbar.update(bytes_transferred/(1024*1024)))
            else:
                bucket.upload_fileobj(file_io, file_name, ExtraArgs={
                                      'Metadata': {'mtime': mtime_str}})
            success = True
            break
        except Exception as e:
            Logger.log.warning(Logger.user+' Uploading to S3 '+path +
                               ' FAILED! retrying(%i,3)...\n%s ' % (trials, str(e)))
            trials = trials - 1

    if not success:
        Logger.log.error(Logger.user+' Uploading to S3 '+path+' ERROR!')
        raise Exception(Logger.user+' Uploading to S3 '+path+' ERROR!')
