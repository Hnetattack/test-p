import socket
import threading

class ChatServer:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 55555
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.users = {}
        self.usernames = []

    def start(self):
        self.server.listen()

        print(f'Server listening on {self.host}:{self.port}')

        while True:
            connection, address = self.server.accept()
            print(f'New connection from {address}')
            threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def handle_client(self, connection, address):
        username = connection.recv(1024).decode()
        self.users[connection] = username
        self.usernames.append(username)
        print(f'{username} has connected')
        self.broadcast(f'{username} has joined the chat!')

        while True:
            message = connection.recv(1024)
            if not message:
                del self.users[connection]
                self.usernames.remove(username)
                print(f'{username} has disconnected')
                self.broadcast(f'{username} has left the chat!')
                break

            message = message.decode()
            self.broadcast(f'{username}: {message}')

        connection.close()

    def broadcast(self, message):
        for user in self.users:
            user.send(message.encode())

if __name__ == '__main__':
    server = ChatServer()
    server.start()