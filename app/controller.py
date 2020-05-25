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
        cur_tup = (row[0], row[0])
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

    return questions, ids

# check if the user's answer is right and return responsing mark
# 0 if not correct, -1 if mark in db is None, full mark if answer is right


def auto_check(answer, que_id):
    conn = sqlite3.connect('app.db')
    print('opened database successfully')
    c = conn.cursor()
    sql_query = "SELECT stand_answer FROM questions WHERE id = '" + \
        str(que_id) + "'"
    c.execute(sql_query)
    std_ans = ''
    for row in c:
        std_ans = row[0]
    std_mark = 0
    sql_query = "SELECT mark FROM questions WHERE id = '" + str(que_id) + "'"
    c.execute(sql_query)
    for row in c:
        std_mark = row[0]
    print('std_ans: ', std_ans, 'std_mark: ',
          std_mark, 'type of mark: ', type(std_mark))
    final_mark = 0
    # if there isn't a standard mark
    if std_ans == '':
        final_mark = -1
    # if the answer is correct
    elif std_ans == answer:
        final_mark = std_mark

    return final_mark

# given tag and user id, return the mark
def get_mark(tag, uid):
    conn = sqlite3.connect('app.db')
    print('opened database successfully')
    c = conn.cursor()
    sql_query = "SELECT answer.mark FROM questions, User, answer where questions.id = question_id " \
                "and questions.tag = '" + tag + "' and  User.id = " + str(uid)
    c.execute(sql_query)
    arr = []
    for row in c:
        if row[0] == -1:
            return 'Assesment is not finished yet!',-1
        arr.append(row[0])
    return arr,sum(arr)

# given a tag of question set, return the mark of that question set
def get_question_mark(tag):
    conn = sqlite3.connect('app.db')
    print('opened database successfully')
    c = conn.cursor()
    sql_query = "SELECT mark FROM questions where questions.tag = '" + tag + "'"
    c.execute(sql_query)
    arr = []
    for row in c:
        arr.append(row[0])
    return arr,sum(arr)

# delete a user using his/her id
def delete_user(user_id):
    conn = sqlite3.connect('app.db')
    print('opened database successfully')
    c = conn.cursor()
    sql_query = "DELETE FROM User where id = " + str(user_id)
    c.execute(sql_query)
    conn.commit()
    sql_query = "DELETE FROM answer where user_id = " + str(user_id)
    c.execute(sql_query)
    conn.commit()
    print('successfully deleted')

# make a user administrator
def make_admin(user_id):
    conn = sqlite3.connect('app.db')
    print('opened database successfully')
    c = conn.cursor()
    sql_query = "UPDATE User SET Is_adm = 1 WHERE id = " + str(user_id)
    c.execute(sql_query)
    conn.commit()
    print('updated successfully')

# get a user's answer for a given question
def get_answer(qid, uid):
    conn = sqlite3.connect('app.db')
    print('opened database successfully')
    c = conn.cursor()
    sql_query = "SELECT content FROM answer where question_id = " + \
        str(qid) + " and user_id = " + str(uid)
    c.execute(sql_query)
    answers = []
    for row in c:
        answers.append(row[0])
    if answers!=[]:
        answers=answers[0].split("\n")
    else:
        answers=["There is no answer!"]
    return answers