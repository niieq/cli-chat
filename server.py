'''
The Chat Server
'''
import socket
import select


class ChatServer:

    def __init__(self, port):
        self.port = port
        self.sockserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockserver.bind(('', self.port))
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
        pass

    def send_message(self):
        pass
