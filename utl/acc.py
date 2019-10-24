#Handles account creation and usage

import sqlite3
from hashlib import md5

__dbfile__ = '../data/sitedata.db'
db = sqlite3.connect(__dbfile__)
c = db.cursor()

c.execute("create table if not exists users (id integer primary_key, username text, password text);")

# #checks account credentials
def verify_acc(un, pw):
    hpw = md5()
    hpw.update(pw.encode('UTF-8'))
    hpw = hpw.hexdigest()
    try:
        userinfo = db.execute('select username, password from users where username= ?', (un,))
    except sqlite3.Error as error:
        print(error)
        return False
    return [item for item in userinfo][0][1] == pw
    
def push_acc(un, pw):
    exists = c.execute("SELECT EXISTS(SELECT 1 FROM users WHERE username=?);", (un,))
    if [boolean for boolean in exists][0][0] == 0:
        uid = count() + 1
        insert(uid, un, pw)
        return True
    return False 

def insert(id, un, pw):
    db.execute('insert into users values (?,?,?);', (id, un, pw))

def count():
    count = c.execute('select count(*) from users;')
    return [num for num in count][0][0]

db.commit()
db.close()