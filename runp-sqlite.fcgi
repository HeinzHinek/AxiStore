#!flask/bin/python

# This is an ugly patch to assure compatibility with older MySQL versions
import MySQLdb as mysql
from config import MYSQL_USER, MYSQL_PASSWORD

con = mysql.connect(host='localhost', user=MYSQL_USER, passwd=MYSQL_PASSWORD)
cur = con.cursor()
cur.execute("SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));")
cur = None
# ugly patch end #


from flup.server.fcgi import WSGIServer
from app import app

if __name__ == '__main__':
    WSGIServer(app).run()