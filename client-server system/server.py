import logging
import socket
import json
import uuid
import time
from _thread import start_new_thread


class SocketServer:

    def __init__(self):
        self.host = "192.168.0.5"
        self.port = 8000
        self.port2 = 8001
        self.unique_code_server = uuid.uuid4()
        self.exp = {}
        self.logger = logging.getLogger('server_client')
        self.logger.setLevel(logging.INFO)
        dates = time.gmtime(time.time())
        self.fh = logging.FileHandler(filename=fr'{dates.tm_year}_{dates.tm_mon}_{dates.tm_mday}.log', encoding='utf8')
        self.fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
        self.fh.setFormatter(formatter)
        self.logger.addHandler(self.fh)

    def run(self):

        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, \
                    socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                s.bind((self.host, self.port))
                s2.bind((self.host, self.port2))

                s.listen(100)
                s2.listen(100)
                conn, addr = s.accept()

                conn2 = None
                start_new_thread(self.threads, (conn, conn2))

                conn2, addr2 = s2.accept()
                conn = None
                start_new_thread(self.threads, (conn, conn2))

    def threads(self, conn1, conn2):
        if conn1 is not None:
            while True:
                id = conn1.recv(1024)
                if not id:
                    break
                self.exp['id'] = id.decode()
                conn1.sendall(str(self.unique_code_server).encode())
        elif conn2 is not None:
            while True:
                data2 = conn2.recv(1024)
                if not data2:
                    break
                message = json.loads(data2)['message']
                unique_code_client = json.loads(data2)['unique_code']
                # unique_code_client = 'aergewr' #TODO for tests
                if str(self.unique_code_server) == unique_code_client:
                    conn2.sendall(b'1')
                    print(message)
                    self.logger.info(message)
                else:
                    conn2.sendall('неверный уникальный код'.encode())


socket_server = SocketServer()
socket_server.run()


