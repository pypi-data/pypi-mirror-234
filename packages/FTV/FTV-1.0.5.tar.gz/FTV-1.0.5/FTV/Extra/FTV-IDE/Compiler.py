import socket

if __name__ == '__main__':
    __PORT = 64328
    __HOST = "localhost"

    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((__HOST, __PORT))
    serv.listen(5)
    while True:
        conn, addr = serv.accept()
        while True:
            data = conn.recv(4096).decode()
            if data:
                print(data)
        conn.close()
        print('client disconnected')
