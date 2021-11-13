import socket
import json
import uuid


def socket_server():
    host = "127.0.0.1"
    port = 8000
    port2 = 8001
    unique_code_server = uuid.uuid4()
    exp = {}

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            s.bind((host, port))
            s2.bind((host, port2))

            s.listen(100)
            s2.listen(100)
            conn, addr = s.accept()
            with conn:
                print("Connected by ", addr)
                while True:
                    id = conn.recv(1024)
                    if not id:
                        break
                    exp['id'] = id.decode()
                    conn.sendall(str(unique_code_server).encode())

            conn2, addr2 = s2.accept()
            with conn2:
                print("Connected by", addr2)
                while True:
                    data2 = conn2.recv(1024)
                    if not data2:
                        break
                    print(data2)
                    message = json.loads(data2)['message']
                    unique_code_client = json.loads(data2)['unique_code']
                    # unique_code_client = 'aergewr' #TODO for tests
                    if str(unique_code_server) == unique_code_client:
                        conn2.sendall(b'1')
                        print('запись в лог')
                    else:
                        conn2.sendall('неверный уникальный код'.encode())


socket_server()


