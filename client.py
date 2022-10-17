import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5678))


class TCPClient:
    nickname = input("Выберите имя пользователя: ")

    def __init__(self, client: socket.socket):
        self.client = client

    def receive(self):
        while True:
            try:
                message = self.client.recv(2**16).decode("utf-8")
                if message == "NICKNAME":
                    self.client.sendall(self.nickname.encode("utf-8"))
                else:
                    print(message)
            except Exception as er:
                print("Error: ", er)
                self.client.close()
                break

    def write(self):
        while True:
            message = "{}: {}".format(self.nickname, input(""))
            self.client.sendall(message.encode("utf-8"))


try:
    receive_thread = threading.Thread(target=TCPClient(client).receive)
    receive_thread.start()
    write_thread = threading.Thread(target=TCPClient(client).write)
    write_thread.start()
except KeyboardInterrupt:
    print(end="\r")
