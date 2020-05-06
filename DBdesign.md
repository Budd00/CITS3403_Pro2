# DB design


1. user
    - id = db.Column(db.Integer, primary_key=True)
    - username = db.Column(db.String(64), index=True, unique=True)
    - email = db.Column(db.String(120), index=True, unique=True)
    - password_hash = db.Column(db.String(128))
    - Is_adm = db.Column(db.bit)
    - mark = db.Column(db.Integer)

2. questions
    - id = db.Column(db.Integer, primary_key=True)
    - content = db.Column(db.String(500), unique=True)
    - stand_answer = db.Column(db.String(500), unique=True)
    - *mark =db.Column(db.Integer)*

3. answer
    - id = db.Column(db.Integer, primary_key=True)
    - question_id db.Column(db.Integer, db.ForeignKey('questions.id'))
    - user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    - content = db.Column(db.String(500), unique=True)