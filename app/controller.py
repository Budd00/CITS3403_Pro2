import sqlite3

# This file contains all the functions to be tested

# get question set tags. e.g: "HTML", "JAVASCRIPT"
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

# get question contents and quesiton ids
def get_questions(tag):
    conn = sqlite3.connect('app.db')
    print('opened database successfully')
    c = conn.cursor()
    sql_query = "SELECT content FROM questions WHERE tag = '" + tag + "'" 
    c.execute(sql_query)
    questions = []
    ids = []
    for row in c:
        questions.append(row[0].split('\n'))
    sql_query = "SELECT id FROM questions WHERE tag = '" + tag + "'" 
    c.execute(sql_query)
    for row in c:
        ids.append(int(row[0]))

    return questions,ids

# check if the user's answer is right and return responsing mark
# 0 if not correct, -1 if mark in db is None, full mark if answer is right
def auto_check(answer, que_id):
    conn = sqlite3.connect('app.db')
    print('opened database successfully')
    c = conn.cursor()
    sql_query = "SELECT stand_answer FROM questions WHERE id = '" + str(que_id) + "'"
    c.execute(sql_query)
    std_ans = ''
    for row in c:
        std_ans = row[0]
    std_mark = 0
    sql_query = "SELECT mark FROM questions WHERE id = '" + str(que_id) + "'"
    c.execute(sql_query)
    for row in c:
        std_mark = row[0]
    print('std_ans: ', std_ans, 'std_mark: ', std_mark, 'type of mark: ', type(std_mark))
    final_mark = 0
    # if there isn't a standard mark
    if std_mark == None:
        final_mark = -1
    # if the answer is correct
    elif std_ans == answer:
        final_mark = std_mark

    return final_mark
