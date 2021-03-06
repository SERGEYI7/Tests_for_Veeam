import socket
import json
import time


def socket_client(ident, message):
    host = "192.168.0.5"
    port = 8000
    port2 = 8001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(str(ident).encode('utf8'))
        unique_code = s.recv(1024)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        exp = {'id': ident, 'unique_code': unique_code.decode(), 'message': message}
        exp_dumps = json.dumps(exp).encode('utf8')
        s2.connect((host, port2))
        s2.sendall(exp_dumps)
        data2 = s2.recv(1024)
        # time.sleep(20)
    if data2.decode() != '1':
        print(data2.decode())


socket_client(ident=1, message='Персональный компьютер')
