import socket
import threading


class TCPServer:
    CLIENTS = []
    NICKNAMES = []

    def __init__(self):
        self._SERVER_HOST = "127.0.0.1"
        self._SERVER_PORT = 5678
        self.server = None

    def __set_bind(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self._SERVER_HOST, self._SERVER_PORT))
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.listen(200)

    def broadcast(self, message):
        for client in self.CLIENTS:
            client.send(message)

    def client_handler(self, client):
        while True:
            try:
                message = client.recv(2**16)
                self.broadcast(message)
            except:
                index = self.CLIENTS.index(client)
                self.CLIENTS.remove(client)
                client.close()
                nickname = self.NICKNAMES[index]
                self.broadcast("{} ушел!".format(nickname).encode("utf-8"))
                self.NICKNAMES.remove(nickname)
                break

    def receive(self):
        self.__set_bind()
        while True:
            client, address = self.server.accept()
            print("Соединён с {}".format(str(address)))
            client.sendall("NICKNAME".encode("utf-8"))
            nickname = client.recv(2**16).decode("utf-8")
            self.NICKNAMES.append(nickname)
            self.CLIENTS.append(client)
            print("Имя пользователя {}".format(nickname))
            self.broadcast("{} присоединился!!!".format(nickname).encode("utf-8"))
            client.sendall("Подключён к серверу!".encode("utf-8"))
            thread = threading.Thread(target=self.client_handler, args=(client,))
            thread.start()


try:
    TCPServer().receive()
except KeyboardInterrupt:
    print(end="\r")
