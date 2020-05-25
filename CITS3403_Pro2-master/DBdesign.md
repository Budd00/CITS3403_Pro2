#pro_2

## DB design

1. user
    - id = db.Column(db.Integer, primary_key=True)
    - username = db.Column(db.String(64), index=True, unique=True)
    - email = db.Column(db.String(120), index=True, unique=True)
    - password_hash = db.Column(db.String(128))
    - Is_adm = db.Column(db.bit)

2. questions
    - id = db.Column(db.Integer, primary_key=True)
    - content = db.Column(db.String(500), unique=True)
    - stand_answer = db.Column(db.String(500), unique=True)
    - tag = db.Column(db.String(20))
    - type = db.Column(db.String(20))
    - *mark =db.Column(db.Integer)*

3. answer
    - id = db.Column(db.Integer, primary_key=True)
    - question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    - user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    - content = db.Column(db.String(500), unique=True)
    - timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    - mark = db.Column(db.Integer,default=-1)

    两种方法，一. 加时间戳，二. 覆盖answers

## pages

- [X] can_login
    1. normal user:
        - [ ] 欢迎用户、介绍、logout
        - [ ] 选择答题（drop list）click之后出——题目以及答案form
            - [ ] 结束
        - [ ] 查分
    2. adm user:
        - [ ] 欢迎用户、介绍、logout
        - [ ] 上传题 （tag、type、题目、标准答案（如果则问答题标准答案为空））
        - [ ] 增删User（flask）
        - [ ] 匿名改卷（ drop list user_id, tag（click事件）->原问题、答案、分数 )
