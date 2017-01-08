'''
The Chat Client
'''
import select
import socket
import sys
from connectdb import connection


def get_or_create(username):
    '''
    If username exists, log in else register user
    '''
    uname = None
    try:
        with connection.cursor() as cursor:
            # look for username
            sql = "SELECT * FROM users WHERE username=%s"
            cursor.execute(sql, username)
            result = cursor.fetchone()
            if result:
                uname = result['username']
            else:
                raise
    except:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (username) VALUES (%s)"
            cursor.execute(sql, username)
        connection.commit()
        uname = result.username
    finally:
        connection.close()
    return uname


def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


class ChatClient:

    def __init__(self, host, port, username):
        self.username = get_or_create(username)
        self.host = host
        self.port = port
        self.csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to remote host
        try:
            self.csocket.connect((self.host, self.port))
        except:
            print('Unable to connect')

            sys.exit()

        print('Connected to remote host. Start sending messages')
        self.csocket.send(bytes(username, 'utf-8'))
        prompt()

    def run(self):
        while True:
            socket_list = [sys.stdin, self.csocket]

            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(
                socket_list, [], [])

            for sock in read_sockets:
                # incoming message from remote server
                if sock == self.csocket:
                    data = sock.recv(1024)
                    if not data:
                        print('\nDisconnected from chat server')
                        sys.exit()
                    else:
                        # print data
                        sys.stdout.write(data.decode('utf-8'))
                        prompt()

                # user entered a message
                else:
                    msg = sys.stdin.readline()
                    self.csocket.send(msg)
                    prompt()


if __name__ == '__main__':
    name = input('Welcome! Enter your username > ')
    cchat = ChatClient('127.0.0.1', 5900, name)
    cchat.run()
