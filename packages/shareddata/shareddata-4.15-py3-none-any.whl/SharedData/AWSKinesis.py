import os
import logging
import boto3
import time
import pytz
import json
from io import StringIO
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

from botocore.exceptions import ClientError

# LOGS


class KinesisLogStreamHandler(logging.StreamHandler):
    # reference: https://docs.python.org/3/library/logging.html#logging.LogRecord
    def __init__(self, user='guest'):
        # By default, logging.StreamHandler uses sys.stderr if stream parameter is not specified
        logging.StreamHandler.__init__(self)

        self.user = user
        self.stream_buffer = []
        self.client = None
        self.stream_name = os.environ['LOG_STREAMNAME']

        if not self.get_client():
            raise Exception('Logging failed check aws credentials!')

        self.create_stream()
        

    def get_client(self):
        success = False
        trials = 3
        while trials>0:
            trials-=1
            try:
                session = boto3.Session(
                    profile_name=os.environ['KINESIS_AWS_PROFILE'])
                if 'KINESIS_ENDPOINT_URL' in os.environ:
                    self.client = session.client('kinesis',
                        endpoint_url=os.environ['KINESIS_ENDPOINT_URL'])
                else:
                    self.client = session.client('kinesis')
                success = True
                break
            except Exception:
                time.sleep(1)
                pass
        return success

    def create_stream(self):

        try:
            self.client.create_stream(
                StreamName=self.stream_name,
                ShardCount=1,
                StreamModeDetails={
                    'StreamMode': 'PROVISIONED'
                }
            )
            time.sleep(10)
        except Exception as e:
            pass


    def emit(self, record):
        try:
            # msg = self.format(record)
            user = os.environ['USERNAME']+'@'+os.environ['COMPUTERNAME']
            timezone = pytz.timezone("UTC")
            dt = datetime.utcfromtimestamp(record.created)
            dt = timezone.localize(dt)
            asctime = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
            msg = {
                'user_name': user,
                'asctime': asctime,
                'logger_name': record.name,
                'level': record.levelname,
                'message': str(record.msg).replace('\'', '\"'),
                # 'function_name': record.funcName,
                # 'file_name': record.filename,
            }
            msg = json.dumps(msg)
            if self.client:
                self.stream_buffer.append({
                    'Data': str(msg).encode(encoding="UTF-8", errors="strict"),
                    'PartitionKey': user,
                })
            else:
                stream = self.stream
                stream.write(msg)
                stream.write(self.terminator)

            self.flush()
        except Exception:
            self.handleError(record)

    def flush(self):
        self.acquire()
        try:
            if self.client and self.stream_buffer:
                self.client.put_records(
                    StreamName=self.stream_name,
                    Records=self.stream_buffer
                )

                self.stream_buffer.clear()
        except Exception as e:
            print("An error occurred during flush operation.")
            print(f"Exception: {e}")
            print(f"Stream buffer: {self.stream_buffer}")

            if not self.get_client():
                raise Exception('Logging failed check aws credentials!')
            
        finally:
            if self.stream and hasattr(self.stream, "flush"):
                self.stream.flush()
            self.release()


class KinesisLogStreamConsumer():
    def __init__(self, user='guest'):
        self.user = user

        self.dflogs = pd.DataFrame([],
                                   columns=['shardid', 'sequence_number', 'user_name', 'asctime', 'logger_name', 'level', 'message'])

        self.lastlogfilepath = Path(os.environ['DATABASE_FOLDER']) / 'Logs'
        self.lastlogfilepath = self.lastlogfilepath / \
            ((datetime.utcnow() + timedelta(days=-1)).strftime('%Y%m%d')+'.log')
        self.last_day_read = False

        self.logfilepath = Path(os.environ['DATABASE_FOLDER']) / 'Logs'
        self.logfilepath = self.logfilepath / \
            (datetime.utcnow().strftime('%Y%m%d')+'.log')
        self.logfileposition = 0

        self.readLogs()

    def read_last_day_logs(self):
        self.last_day_read = True
        if self.lastlogfilepath.is_file():
            try:
                _dflogs = pd.read_csv(self.lastlogfilepath, header=None, sep=';',
                                      engine='python', on_bad_lines='skip')
                _dflogs.columns = ['shardid', 'sequence_number',
                                   'user_name', 'asctime', 'logger_name', 'level', 'message']
                self.dflogs = pd.concat([_dflogs, self.dflogs], axis=0)
            except:
                pass

    def readLogs(self):
        if not self.last_day_read:
            self.read_last_day_logs()

        _logfilepath = Path(os.environ['DATABASE_FOLDER']) / 'Logs'
        _logfilepath = _logfilepath / \
            (datetime.utcnow().strftime('%Y%m%d')+'.log')
        if self.logfilepath != _logfilepath:
            self.logfileposition = 0
            self.logfilepath = _logfilepath

        if self.logfilepath.is_file():
            try:
                with open(self.logfilepath, 'r') as file:
                    file.seek(self.logfileposition)
                    newlines = '\n'.join(file.readlines())
                    dfnewlines = pd.read_csv(StringIO(newlines), header=None, sep=';',
                                             engine='python', on_bad_lines='skip')
                    dfnewlines.columns = [
                        'shardid', 'sequence_number', 'user_name', 'asctime', 'logger_name', 'level', 'message']
                    self.dflogs = pd.concat([self.dflogs, dfnewlines])
                    self.logfileposition = file.tell()
            except:
                pass

        return self.dflogs

    def getLogs(self):
        df = self.readLogs()
        if not df.empty:
            idxhb = np.array(['#heartbeat#' in s for s in df['message']])
            idshb = np.where(idxhb)[0]
            if len(idshb > 100):
                idshb = idshb[-100:]
            ids = np.where(~idxhb)[0]
            ids = np.sort([*ids, *idshb])
            df = df.iloc[ids, :]
        return df

    def connect(self):
        try:
            session = boto3.Session(
                profile_name=os.environ['KINESIS_AWS_PROFILE'])
            if 'KINESIS_ENDPOINT_URL' in os.environ:
                self.client = session.client('kinesis',
                                             endpoint_url=os.environ['KINESIS_ENDPOINT_URL'])
            else:
                self.client = session.client('kinesis')
        except:
            print('Could not connect to AWS!')
            return False

        try:
            print("Trying to create stream %s..." %
                  (os.environ['LOG_STREAMNAME']))
            self.client.create_stream(
                StreamName=os.environ['LOG_STREAMNAME'],
                ShardCount=1,
                StreamModeDetails={
                    'StreamMode': 'PROVISIONED'
                }
            )
            time.sleep(10)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print("Stream already exists")
            else:
                print("Trying to create stream unexpected error: %s" % e)
                pass

        try:
            self.stream = self.client.describe_stream(
                StreamName=os.environ['LOG_STREAMNAME'])
        except:
            print('Could not describe stream!')
            return False

        if self.stream and 'StreamDescription' in self.stream:
            self.stream = self.stream['StreamDescription']
            for i in range(len(self.stream['Shards'])):
                readfromstart = True
                shardid = self.stream['Shards'][i]['ShardId']
                if not self.dflogs.empty and (shardid in self.dflogs['shardid'].values):
                    readfromstart = False
                    seqnum = self.dflogs[self.dflogs['shardid']
                                         == shardid].iloc[-1]['sequence_number']
                    try:
                        shard_iterator = self.client.get_shard_iterator(
                            StreamName=self.stream['StreamName'],
                            ShardId=self.stream['Shards'][i]['ShardId'],
                            ShardIteratorType='AFTER_SEQUENCE_NUMBER',
                            StartingSequenceNumber=seqnum
                        )
                    except:
                        print(
                            'Failed retrieving shard iterator, reading from start...')
                        readfromstart = True

                if readfromstart:
                    print('############### READING FROM START ###############')
                    start_of_day = pd.Timestamp.utcnow().floor('D').timestamp()

                    shard_iterator = self.client.get_shard_iterator(
                                        StreamName=self.stream['StreamName'],
                                        ShardId=self.stream['Shards'][i]['ShardId'],
                                        ShardIteratorType='AT_TIMESTAMP',
                                        Timestamp=start_of_day
                                    )
                    
                self.stream['Shards'][i]['ShardIterator'] = shard_iterator['ShardIterator']
        else:
            print('Failed connecting StreamDescriptor not found!')
            return False

        return True

    def consume(self):
        try:
            for i in range(len(self.stream['Shards'])):
                response = self.client.get_records(
                    ShardIterator=self.stream['Shards'][i]['ShardIterator'],
                    Limit=1000)
                self.stream['Shards'][i]['ShardIterator'] = response['NextShardIterator']
                if len(response['Records']) > 0:
                    for r in response['Records']:
                        try:
                            rec = r['Data'].decode(
                                encoding="UTF-8", errors="strict")
                            rec = json.loads(rec.replace(
                                "\'", "\"").replace(';', ','))

                            line = '%s;%s;%s;%s;%s;%s;%s' % (self.stream['Shards'][i]['ShardId'],
                                                             r['SequenceNumber'], rec['user_name'], rec['asctime'],
                                                             rec['logger_name'], rec['level'], rec['message'])

                            dt = datetime.strptime(
                                rec['asctime'][:-5], '%Y-%m-%dT%H:%M:%S')

                            logfilepath = Path(
                                os.environ['DATABASE_FOLDER']) / 'Logs'
                            logfilepath = logfilepath / \
                                (dt.strftime('%Y%m%d')+'.log')
                            if not logfilepath.parents[0].is_dir():
                                os.makedirs(logfilepath.parents[0])

                            with open(logfilepath, 'a+', encoding='utf-8') as f:
                                f.write(line.replace(
                                    '\n', ' ').replace('\r', ' ')+'\n')
                                f.flush()

                        except Exception as e:
                            print('Invalid record:%s\nerror:%s' %
                                  (str(rec), str(e)))
            return True
        except:
            return False

# REAL TIME


class KinesisStreamProducer():
    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.client = None
        self.stream_buffer = []
        try:
            session = boto3.Session(
                profile_name=os.environ['KINESIS_AWS_PROFILE'])
            if 'KINESIS_ENDPOINT_URL' in os.environ:
                self.client = session.client('kinesis',
                                                 endpoint_url=os.environ['KINESIS_ENDPOINT_URL'])
            else:
                self.client = session.client('kinesis')
        except Exception:
            print('Kinesis client initialization failed.')

        try:
            self.client.create_stream(
                StreamName=stream_name,
                ShardCount=1,
                StreamModeDetails={
                    'StreamMode': 'PROVISIONED'
                }
            )
            time.sleep(10)
        except Exception as e:
            pass

    def produce(self, record, partitionkey):
        _rec = json.dumps(record)
        self.stream_buffer.append({
            'Data': str(_rec).encode(encoding="UTF-8", errors="strict"),
            'PartitionKey': partitionkey,
        })
        self.client.put_records(
            StreamName=self.stream_name,
            Records=self.stream_buffer
        )
        self.stream_buffer = []


class KinesisStreamConsumer():
    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.stream_buffer = []
        self.last_sequence_number = None
        self.get_stream()

    def get_stream(self):
        session = boto3.Session()
        if 'KINESIS_ENDPOINT_URL' in os.environ:
            self.client = session.client(
                'kinesis', endpoint_url=os.environ['KINESIS_ENDPOINT_URL'])
        else:
            self.client = session.client('kinesis')

        try:
            self.client.create_stream(
                StreamName=self.stream_name,
                ShardCount=1,
                StreamModeDetails={
                    'StreamMode': 'PROVISIONED'
                }
            )
            time.sleep(10)
        except Exception as e:
            pass

        self.stream = self.client.describe_stream(StreamName=self.stream_name)
        if self.stream and 'StreamDescription' in self.stream:
            self.stream = self.stream['StreamDescription']
            i = 0
            for i in range(len(self.stream['Shards'])):
                shardid = self.stream['Shards'][i]['ShardId']
                if self.last_sequence_number is None:
                    shard_iterator = self.client.get_shard_iterator(
                        StreamName=self.stream['StreamName'],
                        ShardId=shardid,
                        ShardIteratorType='LATEST'
                    )
                else:
                    try:
                        shard_iterator = self.client.get_shard_iterator(
                            StreamName=self.stream['StreamName'],
                            ShardId=shardid,
                            ShardIteratorType='AFTER_SEQUENCE_NUMBER',
                            StartingSequenceNumber=self.last_sequence_number
                        )
                    except:
                        print('############### RESETING SHARD ITERATOR SEQUENCE ###############')
                        shard_iterator = self.client.get_shard_iterator(
                            StreamName=self.stream['StreamName'],
                            ShardId=shardid,
                            ShardIteratorType='LATEST'
                        )

                self.stream['Shards'][i]['ShardIterator'] = shard_iterator['ShardIterator']

        if self.stream['StreamStatus'] != 'ACTIVE':
            raise Exception('Stream status %s' % (self.stream['StreamStatus']))

    def consume(self):
        success = False

        for i in range(len(self.stream['Shards'])):
            try:
                response = self.client.get_records(
                    ShardIterator=self.stream['Shards'][i]['ShardIterator'],
                    Limit=100)
                success = True
                self.stream['Shards'][i]['ShardIterator'] = response['NextShardIterator']
                if len(response['Records']) > 0:
                    for r in response['Records']:
                        try:
                            rec = json.loads(r['Data'])
                            self.last_sequence_number = r['SequenceNumber']
                            self.stream_buffer.append(rec)
                        except Exception as e:
                            print('Invalid record:'+str(r['Data']))
                            print('Invalid record:'+str(e))

            except Exception as e:
                print('Kinesis consume exception:%s' % (e))
                break

        return success
