from lib.socket import Server

host = 'localhost'
port = 8001

if __name__ == '__main__':
    # Server code:
    server = Server(host, port)
    server.accept()
    while True:
        try:
            data = server.recv()
            print('server data received' + data)
            server.send({'result': 'hello world'}).close()
        except:
            server.close()
