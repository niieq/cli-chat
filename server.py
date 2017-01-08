'''
The Chat Server
'''
import select
import socket
from connectdb import connection


def save_message(message, user):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO messages (username, message) VALUES (%s, %s)"
            cursor.execute(sql, (user, message))
        connection.commit()
    except:
        print('Didn\'t save. Try Again')


class ChatServer:

    def __init__(self, port):
        self.port = port
        self.sockserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockserver.bind(('', self.port))
        self.sockserver.listen(5)

        self.connectors = {}
        self.connectors[self.sockserver] = 'server'
        print('Chatserver started on port {}'.format(self.port))

    def run(self):
        while True:
            read_sockets, write_sockets, error_sockets = select.select(
                self.connectors.keys(), [], [])

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
                        del self.connectors[sock]
                    else:
                        # host, port = sock.getpeername()
                        _user = self.connectors[sock]
                        msg = data.decode('utf-8')
                        if msg.find(':') != -1:
                            for k, v in self.connectors.items():
                                if v == msg.split(':')[0]:
                                    _to = k
                                    break
                            self.send_message(msg.split(':')[1], _to, _user)
                        else:
                            newstr = '{}'.format(data)
                            self.broadcast_string(newstr, sock)

    def accept_new_connection(self):
        newsock, (remhost, remport) = self.sockserver.accept()
        username = newsock.recv(1024).decode('utf-8')
        self.connectors[newsock] = username
        # newsock.send(bytes("You're connected to the chatserver\r\n", 'utf-8'))
        status = '{} is online \r\n'.format(username)
        self.broadcast_string(status, newsock)

    def broadcast_string(self, msg, omit_sock):
        for sock in self.connectors.keys():
            if sock != self.sockserver and sock != omit_sock:
                try:
                    sock.send(bytes(msg, 'utf-8'))
                except:
                    sock.close()
                    del self.connectors[sock]

    def send_message(self, msg, receiver, sender):
        modified_msg = '{} > {}'.format(sender, msg.lstrip())
        receiver.send(bytes(modified_msg, 'utf-8'))
        save_message(msg.lstrip(), sender)


if __name__ == '__main__':
    schat = ChatServer(5400)
    schat.run()
