import socket
import select


class TCPServer:
    _CLIENTS = []
    _FOR_READ = []
    __SERVER_HOST = "127.0.0.1"
    __SERVER_PORT = 5678

    def __init__(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.__SERVER_HOST, self.__SERVER_PORT))
        self._server.listen(200)

    def broadcast(self, message):
        for client in self._CLIENTS:
            client.send(message)

    def receive(self, r_socket):
        client, address = r_socket.accept()
        print("Client connected: ", address)
        self._FOR_READ.append(client)
        self._CLIENTS.append(client)

    def run(self):
        while True:
            reading, _, errors = select.select(self._FOR_READ + [self._server], [], self._FOR_READ)
            for r in reading:
                if r is not self._server:
                    try:
                        data = r.recv(2**16)
                    except ConnectionResetError:
                        r.close()
                    else:
                        self.broadcast(data)

                else:
                    self.receive(r)

            for e in errors:
                print(e.fileno())
                self._FOR_READ.remove(e)
                e.close()


try:
    TCPServer().run()
except KeyboardInterrupt:
    print(end="\r")
