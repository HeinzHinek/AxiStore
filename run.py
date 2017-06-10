#!flask/bin/python

# This is an ugly patch to assure compatibility with older MySQL versions
import MySQLdb as mysql
from config import MYSQL_USER, MYSQL_PASSWORD

con = mysql.connect(host='localhost', user=MYSQL_USER, passwd=MYSQL_PASSWORD)
cur = con.cursor()
cur.execute("SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));")
cur = None
# ugly patch end #

from app import app
app.run(debug=True)
