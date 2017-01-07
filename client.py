'''
The Chat Client
'''
import socket
import select


class ChatClient:

    def __init__(self, username):
        self.username = username
