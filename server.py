'''
The Chat Server
'''
import select
import socket


class ChatServer:

    def __init__(self, port):
        self.port = port
        self.sockserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockserver.bind(('', self.port))
        self.sockserver.listen(5)

        self.connectors = {}
        self.connectors['server'] = self.sockserver
        print('Chatserver started on port {}'.format(self.port))

    def run(self):
        while True:
            read_sockets, write_sockets, error_sockets = select.select(
                self.connectors.values(), [], [])

            for sock in read_sockets:

                if sock == self.sockserver:
                    self.accept_new_connection()
                else:
                    data = sock.recv(1024)
                    if data == '':
                        host, port = sock.getpeername()
                        status = 'Client left {}:{}\r\n'.format(host, port)
                        self.broadcast_string(status, sock)
                        sock.close()
                        for k, v in self.connectors.items():
                            if v == sock:
                                del self.connectors[k]
                    else:
                        host, port = sock.getpeername()
                        newstr = '[{}:{}] {}'.format(host, port, data)
                        self.broadcast_string(newstr, sock)

    def accept_new_connection(self):
        newsock, (remhost, remport) = self.sockserver.accept()
        username = newsock.recv(1024).decode('utf-8')
        self.connectors[username] = newsock
        newsock.send(bytes("You're connected to the chatserver\r\n", 'utf-8'))
        status = 'Client joined {}:{}\r\n'.format(remhost, remport)
        self.broadcast_string(status, newsock)

    def broadcast_string(self, msg, omit_sock):
        for sock in self.connectors.values():
            if sock != self.sockserver and sock != omit_sock:
                try:
                    sock.send(bytes(msg, 'utf-8'))
                except:
                    sock.close()
                    for k, v in self.connectors.items():
                        if v == sock:
                            del self.connectors[k]

    def send_message(self, msg, receiver):
        host = self.sockserver.getpeername()[0]
        modified_msg = '[{} says ] {}'.format(host, msg)
        receiver.send(modified_msg)


if __name__ == '__main__':
    schat = ChatServer(5900)
    schat.run()
