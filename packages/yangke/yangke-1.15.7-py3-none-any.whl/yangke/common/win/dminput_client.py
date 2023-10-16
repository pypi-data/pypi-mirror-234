from xmlrpc.client import ServerProxy

if __name__ == '__main__':
    server = ServerProxy("http://localhost:8888")
    server.click(1, 2)
