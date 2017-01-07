'''
The Chat Server
'''
import socket


class ChatServer:

    def __init__(self, port):
        self.port = port
        self.sockserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockserver.bind(('', self.port))
        self.sockserver.listen(5)

        self.connectors = [self.sockserver]
        print('Chatserver started on port {}'.format(self.port))

    def run(self):
        pass

    def accept_new_connection(self):
        pass

    def send_message(self):
        pass
