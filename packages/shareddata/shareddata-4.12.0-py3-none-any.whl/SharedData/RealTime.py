import socket
import threading
import time
import select
import numpy as np


from SharedData.Logger import Logger


class RealTime():

    # Dict to keep track of all connected client sockets
    clients = {}
    # Create a lock to protect access to the clients Dict
    lock = threading.Lock()
    server = None
    shdata = None
    accept_clients = None

    @staticmethod
    def runserver(shdata, host, port):

        RealTime.shdata = shdata

        RealTime.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # This line allows the address to be reused
        RealTime.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Create the server and start accepting clients in a new thread
        RealTime.accept_clients = threading.Thread(
            target=RealTime.accept_clients_thread, args=(host, port))
        RealTime.accept_clients.start()

    @staticmethod
    def accept_clients_thread(host, port):
        RealTime.server.bind((host, port))
        RealTime.server.listen()

        Logger.log.info(f'Listening on {host}:{port}')

        while True:
            conn, addr = RealTime.server.accept()
            threading.Thread(target=RealTime.handle_client_thread,
                             args=(conn, addr)).start()

    @staticmethod
    def handle_client_thread(conn, addr):
        Logger.log.info(f"New client connected: {addr}")

        # Add the client socket to the list of connected clients
        with RealTime.lock:
            RealTime.clients[conn] = {
                'watchdog': time.time_ns()
            }

        sockdata = RealTime.clients[conn]
        try:
            while True:
                try:
                    # Check if there is data ready to be read from the client
                    ready_to_read, _, _ = select.select([conn], [], [], 0)
                    if ready_to_read:
                        # Receive data from the client
                        data = conn.recv(1024)
                        if data:
                            # clear watchdog
                            sockdata['watchdog'] = time.time_ns()
                            data = data.decode()
                            msg = data.split('#')[1].split(',')
                            msgtype = msg[0]
                            if msgtype == 'subscribe':
                                database = msg[1]
                                period = msg[2]
                                source = msg[3]
                                container = msg[4]
                                if container == 'table':
                                    tablename = msg[5]
                                    Logger.log.info('Serving updates of %s/%s/%s/%s' %
                                                    (database, period, source, tablename))
                                    sockdata['table'] = RealTime.shdata.table(
                                        database, period, source, tablename)
                                    sockdata['count'] = int(msg[6])
                                    timestamp = float(msg[7])
                                    datetime_ns = np.datetime64(
                                        int(timestamp), 's')
                                    datetime_ns += np.timedelta64(
                                        int((timestamp % 1)*1e9), 'ns')
                                    sockdata['mtime'] = datetime_ns
                                    table = sockdata['table']
                                    sockdata['maxrows'] = int(
                                        np.floor(1024/table.itemsize))
                        else:                            
                            break

                    if 'table' in sockdata:
                        table = sockdata['table']
                        ids2send = []

                        lastmtime = sockdata['mtime']
                        lookbackid = table.count-1000
                        if lookbackid < 0:
                            lookbackid = 0
                        updtids = np.where(
                            table[lookbackid:]['mtime'] > lastmtime)
                        if len(updtids) > 0:
                            ids2send.extend(updtids[0]+lookbackid)
                            sockdata['mtime'] = max(
                                table[lookbackid:]['mtime'])

                        lastcount = sockdata['count']
                        curcount = table.count.copy()
                        if curcount > lastcount:
                            newids = np.arange(lastcount, curcount)
                            ids2send.extend(newids)
                            sockdata['count'] = curcount

                        if len(ids2send) > 0:
                            ids2send = np.unique(ids2send)
                            ids2send = np.sort(ids2send)
                            maxrows = sockdata['maxrows']
                            rows2send = len(ids2send)
                            sentrows = 0
                            while sentrows < rows2send:
                                msgsize = min(maxrows, rows2send)
                                msg = table[ids2send[sentrows:sentrows +
                                                     msgsize]].tobytes()
                                conn.sendall(msg)
                                sentrows += msgsize
                            # clear watchdog
                            sockdata['watchdog'] = time.time_ns()

                    time.sleep(0.0001)
                except Exception as e:
                    Logger.log.error(
                        'Client {addr} disconnected with error:%s' % (e))
                    break
        finally:
            with RealTime.lock:
                RealTime.clients.pop(conn)
            Logger.log.info(f"Client {addr} disconnected.")
            conn.close()

    @staticmethod
    def table_subscribe_thread(table, host, port):

        shnumpy = table.records
        buffsize = int(np.floor(1024/shnumpy.itemsize))*shnumpy.itemsize
        bytes_buffer = bytearray()

        while True:
            try:
                client_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((host, port))
                msg = '#subscribe,%s,%s,%s,table,%s,%i,%.6f#' % \
                    (table.database, table.period, table.source,
                     table.tablename, int(shnumpy.count), float(shnumpy.mtime))
                msgb = msg.encode('utf-8')
                data = client_socket.send(msgb)
                while True:
                    try:
                        # Receive data from the server
                        data = client_socket.recv(buffsize)
                        if data == b'':
                            msg = 'Subscription %s,%s,%s,table,%s closed !' % \
                                (table.database, table.period,
                                 table.source, table.tablename)
                            Logger.log.warning(msg)
                            client_socket.close()
                        else:
                            bytes_buffer.extend(data)

                            # while we have enough data for at least one record
                            while len(bytes_buffer) >= shnumpy.itemsize:
                                # take the first record's worth of bytes
                                record_data = bytes_buffer[:shnumpy.itemsize]
                                # and remove them from the buffer
                                del bytes_buffer[:shnumpy.itemsize]
                                rec = np.frombuffer(
                                    record_data, dtype=shnumpy.dtype)
                                shnumpy.upsert(rec)

                    except Exception as e:
                        msg = 'Subscription %s,%s,%s,table,%s error!\n%s' % \
                            (table.database, table.period,
                             table.source, table.tablename, str(e))
                        Logger.log.error(msg)
                        client_socket.close()
                        break
            except Exception as e:
                msg = 'Retrying subscription %s,%s,%s,table,%s!\n%s' % \
                    (table.database, table.period,
                     table.source, table.tablename, str(e))
                Logger.log.warning(msg)
                time.sleep(5)
