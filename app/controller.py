import sqlite3
from app.models import questions

# This file contains all the functions to be tested

def get_tags():
    #connect to database
    conn = sqlite3.connect('app.db')
    print('opened database successfully')
    c = conn.cursor()
    cursor = c.execute("SELECT DISTINCT tag FROM questions")
    tags = []
    for row in cursor:
        cur_tup = (row[0],row[0])
        tags.append(cur_tup)
    return tags


def get_questions(tag):
    conn = sqlite3.connect('app.db')
    print('opened database successfully')
    c = conn.cursor()
    sql_query = "SELECT content FROM questions WHERE tag = '" + tag + "'"
    c.execute(sql_query)
    questions = []
    for row in c:
        questions.append(row[0].split('\n'))
    return questions
