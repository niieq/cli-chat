'''
The Chat Server
'''
import socket
import select


class ChatServer:

    def __init__(self, port):
        self.port = port
        self.sockserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockserver.bind(('0.0.0.0', self.port))
        self.sockserver.listen(5)

        self.connectors = [self.sockserver]
        print('Chatserver started on port {}'.format(self.port))

    def run(self):
        while True:
            read_sockets, write_sockets, error_sockets = select.select(
                self.connectors, [], [])

            for sock in read_sockets:

                if sock == self.sockserver:
                    self.accept_new_connection()
                else:
                    data = sock.recv(4096)
                    if data == '':
                        host, port = sock.getpeername()
                        status = 'Client left {}:{}\r\n'.format(host, port)
                        self.broadcast_string(status, sock)
                        sock.close()
                        self.connectors.remove(sock)
                    else:
                        host, port = sock.getpeername()
                        newstr = '[{}:{}] {}' % (host, port, data)
                        self.broadcast_string(newstr, sock)

    def accept_new_connection(self):
        newsock, (remhost, remport) = self.sockserver.accept()
        self.connectors.append(newsock)
        newsock.send("You're connected to the Python chatserver\r\n")
        status = 'Client joined %s:%s\r\n' % (remhost, remport)
        self.broadcast_string(status, newsock)

    def broadcast_string(self, msg, omit_sock):
        for sock in self.descriptors:
            if sock != self.sockserver and sock != omit_sock:
                sock.send(msg)

    def send_message(self, msg, receiver):
        host = self.sockserver.getpeername()[0]
        modified_msg = '[{} says ] {}'.format(host, msg)
        receiver.send(modified_msg)


if __name__ == '__main__':
    schat = ChatServer(5600)
    schat.run()
