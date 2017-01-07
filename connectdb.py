'''
Database Connection
'''
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='admin',
                             db='clichat',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
