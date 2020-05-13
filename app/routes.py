from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import logout_user, login_user, current_user, login_required
from app.models import User, questions,answer
from app import app, db, controller
from app.Form import LoginForm, RegistrationForm, TagForm, AnswerForm
from werkzeug.urls import url_parse


# app = Flask(__name__)
app.secret_key = 'SECRET KEY'
@app.route('/')
@app.route('/index')
def index():
    return render_template('Application.html')


@app.route('/Login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('get_test'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('welcome')
        return redirect(next_page)
    return render_template('Can_log.html', title='Sign In', form=form)

@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    form = LoginForm()
    return render_template('Admin_log.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/test', methods=['GET', 'POST'])
@login_required
def get_test():
    tags = controller.get_tags()
    print('tags are: ', tags)
    form = TagForm()
    tagvalue = None
    if form.validate_on_submit():
        tagvalue = form.tag.data
        return redirect(url_for('Que',tag=tagvalue, index="0"))
    return render_template('test.html', title='test', form=form)


@app.route('/questions?tag=<tag>&index=<index>', methods=['GET', 'POST'])
@login_required
def Que(tag,index):
    index=int(index)
    form = AnswerForm()
    ques,ids = controller.get_questions(tag)
    limit=len(ques)
    que=ques[index]
    que_id=ids[index]
    if index>=limit-1:
        limit=0
    if form.validate_on_submit():
        content = form.answer.data
        user_id = current_user.get_id()
        mark= controller.auto_check(content,que_id)
        flash("Answer saved!")
        Answer = answer(question_id=que_id,user_id=user_id,content=content,mark=mark)
        old_answer = answer.query.filter_by( question_id=que_id, user_id=user_id).first()
        if old_answer!= None:
            db.session.delete(old_answer)
            db.session.commit()
        db.session.add(Answer)
        db.session.commit()
           
    return render_template('Questions.html', title='Questions', form=form,question=que,tag=tag, nextindex=str(index+1),lastindex=str(index-1),limit=limit)
    


@app.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    return render_template('welcome.html', title='Home')


@app.route('/mark', methods=['GET', 'POST'])
@login_required
def mark():
    return render_template('mark.html', title='mark')


@app.route('/ending', methods=['GET', 'POST'])
@login_required
def ending():
    return render_template('endingpage.html', title='End_quiz')
