import sqlite3

# This file contains all the functions to be tested

def get_tags():
    #connect to database
    conn = sqlite3.connect('app.db')
    print('opened database successfully')
    c = conn.cursor()
    cursor = c.execute("SELECT DISTINCT tag FROM questions")
    tags = []
    for row in cursor:
        tags.append(row[0])
    return tags