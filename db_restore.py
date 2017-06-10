# -*- coding: utf-8 -*-
import os
import MySQLdb as mysql
from subprocess import call

from config import basedir, MYSQL_USER, MYSQL_PASSWORD


BACKUP_DIR = os.path.join(basedir, 'db_backup')

if not os.path.isdir(BACKUP_DIR):
    print 'There has to be a directory in the project root directory called "db_backup" ' \
          'for this script to work!'
    exit(1)

files = os.listdir(BACKUP_DIR)
if len(files) != 1:
    print 'There has to be exactly one sql backup file in the "db_backup" directory ' \
          'for this script to work!'

backup_file_path = os.path.join(BACKUP_DIR, files[0])

con = mysql.connect(host='localhost', user=MYSQL_USER, passwd=MYSQL_PASSWORD)
cur = con.cursor()
cur.execute('drop database if exists apps;')
cur.execute('create database apps character set utf8 collate utf8_bin;')

command = 'mysql -u %s -p%s apps < %s' % (MYSQL_USER, MYSQL_PASSWORD, backup_file_path)

return_code = call(command, shell=True)

if return_code > 0:
    print 'Database could not be restored! Error code: %s' % return_code
    exit(return_code)

print 'Database has been successfully restored!'
exit(0)
