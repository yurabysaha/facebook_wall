import sqlite3 as db

c = db.connect(database="../db")
cu = c.cursor()
try:
    cu.execute("""
          CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fb_id VARCHAR,
            name VARCHAR,
            token TEXT,
            fatch_all BOOLEAN DEFAULT FALSE 
            );
    """)
except db.DatabaseError, x:
    print "DB Error: ", x
c.commit()
c.close()

c = db.connect(database="../db")
cu = c.cursor()
try:
    cu.execute("""
          CREATE TABLE groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link VARCHAR,
            owner VARCHAR,
            fatch BOOLEAN DEFAULT FALSE 
            );
    """)
except db.DatabaseError, x:
    print "DB Error: ", x
c.commit()
c.close()

def add_new_user(token, fb_data):
    con = db.connect(database="../db")
    cur = con.cursor()
    query = "INSERT INTO users (fb_id, name, token) values (?, ?, ?)"
    cur.execute(query, (fb_data['id'], fb_data['name'], token, ))
    con.commit()
    con.close()

def add_new_group(link, owner):
    con = db.connect(database="../db")
    cur = con.cursor()
    query = "INSERT INTO groups (link, owner) values (?, ?)"
    cur.execute(query, (link, owner, ))
    con.commit()
    con.close()
