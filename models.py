import sqlite3 as sql
from flask import current_app
import forms
con = sql.connect("test1.db",check_same_thread=False)
cur = con.cursor()
cur.executescript('drop table if exists users;')
cur.execute("create table users( id integer primary key autoincrement, username text not null, password text not null);")
def insertUser(username,password):


    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (str(username), str(password),))
    con.commit()
    con.close()


def retrieveUsers():
	con = sql.connect("test1.db")
	cur = con.cursor()
	cur.execute("SELECT username, password FROM users")
	users = cur.fetchall()
	con.close()
	return users