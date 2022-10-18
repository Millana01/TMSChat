import socket
import threading


class TCPClient:
    _START_SESSION = True
    NICKNAME = input("Enter your name: ")
    NICKNAMES = []

    def __init__(self):
        self._host = '127.0.0.1'
        self._port = 5678
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self._host, self._port))

    def receive(self):
        while True:
            try:
                if self._START_SESSION:
                    self._START_SESSION = False
                    self.NICKNAMES.append(self.NICKNAME)
                    continue
                message = self.client.recv(1024).decode('utf-8')
                print(message)
            except Exception as err:
                print("Error: ", err)
                self.client.close()
                break

    def write(self):
        while True:  # Вывод сообщений в чат
            message = '{}: {}'.format(self.NICKNAME, input(''))
            self.client.send(message.encode('utf-8'))


try:
    receive_thread = threading.Thread(target=TCPClient().receive)
    receive_thread.start()
    write_thread = threading.Thread(target=TCPClient().write)
    write_thread.start()
except KeyboardInterrupt:
    print(end="\r")
