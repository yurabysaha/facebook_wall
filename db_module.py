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
            scrup_all BOOLEAN DEFAULT 0 
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
            scrup BOOLEAN DEFAULT 0 
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

def update_group_fetch(id, status):
    con = db.connect(database="../db")
    cur = con.cursor()
    query = "UPDATE groups SET scrup=? WHERE id=?"
    cur.execute(query, (status, id,))
    con.commit()
    con.close()
