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
# Create table for data_posts
c = db.connect(database="../db")
cu = c.cursor()
try:
    cu.execute("""
          CREATE TABLE data_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR,
            user_name VARCHAR,
            group_id VARCHAR,
            group_name VARCHAR,
            created_post_time DATETIME,
            who_created_name VARCHAR,
            who_created_id VARCHAR,
            post_description VARCHAR,
            post_message VARCHAR,
            post_pict_link VARCHAR,
            post_content_link VARCHAR,
            post_source VARCHAR,
            post_id VARCHAR,
            post_story VARCHAR,
            created_at datetime  NOT NULL  DEFAULT current_timestamp,
            updated_at datetime  NOT NULL  DEFAULT current_timestamp
            );
    """)
except db.DatabaseError, x:
    print "DB Error: ", x
c.commit()
c.close()
#-----------------------------
def add_new_user(token, fb_data):
    con = db.connect(database="../db")
    cur = con.cursor()
    query = "INSERT INTO users (fb_id, name, token) values (?, ?, ?)"
    cur.execute(query, (fb_data['id'], fb_data['name'], token, ))
    con.commit()
    con.close()

def add_new_posts(user_id, user_name, group_id, group_name, post):
    con = db.connect(database="../db")
    cur = con.cursor()
    query = "INSERT INTO data_posts (user_id, user_name, group_id, group_name, created_post_time, who_created_id, who_created_name, post_description, post_message, post_pict_link, post_content_link, post_source, post_id, post_story) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cur.execute(query, (user_id, user_name, group_id, group_name, post['created_time'], post['from']['id'],  post['from']['name'], post['description'], post['message'], post['picture'], post['link'], post['source'], post['id'], post['story'], ))
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
