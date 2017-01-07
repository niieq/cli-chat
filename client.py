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
            uname = result['username']
    except:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (username) VALUES (%s)"
            cursor.execute(sql, username)
        connection.commit()
        uname = result.username
    finally:
        connection.close()
    return uname


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


if __name__ == '__main__':
    print(get_or_create('nii'))
