#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from config import MYSQL_USER, MYSQL_PASSWORD
from app import db
import os.path
import MySQLdb as mysql


con = mysql.connect(host='localhost', user=MYSQL_USER, passwd=MYSQL_PASSWORD)
cur = con.cursor()
cur.execute('drop database apps;')
cur.execute('create database apps character set utf8 collate utf8_bin;')


db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))