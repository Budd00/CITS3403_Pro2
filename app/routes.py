from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import logout_user, login_user, current_user, login_required
from app.models import User, questions,answer
from app import app, db, controller
from app.Form import LoginForm, RegistrationForm,AnswerForm,QuestionForm,MarkForm
from werkzeug.urls import url_parse
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired


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
        if user.Is_adm ==1:
            next_page = url_for('AdminWelcome')
        return redirect(next_page)
    return render_template('Can_log.html', title='Sign In', form=form)


@app.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    return render_template('welcome.html', title='Home')

@app.route('/AdminWelcome', methods=['GET', 'POST'])
def AdminWelcome():
    return render_template('AdminWelcome.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('welcome'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        if current_user.is_authenticated:
            flash('Add a user')
        else:
            flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/test', methods=['GET', 'POST'])
@login_required
def get_test():
    class TagForm(FlaskForm):
        pass

    setattr(TagForm, 'tag', SelectField(validators=[
            DataRequired('Please select a tag')], choices=controller.get_tags()))
    setattr(TagForm, 'submit', SubmitField('get quiz'))
    form = TagForm()
    tags = controller.get_tags()
    print('tags are: ', tags)
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




@app.route('/mark', methods=['GET', 'POST'])
@login_required
def mark():
    class TagForm(FlaskForm):
        pass
    setattr(TagForm, 'tag', SelectField(validators=[
            DataRequired('Please select a tag')], choices=controller.get_tags()))
    setattr(TagForm, 'submit', SubmitField('get quiz'))
    form = TagForm()
    mark=[(0,0)]
    mark_sum=0
    weight_sum=0
    if form.validate_on_submit():
        mark, mark_sum = controller.get_mark(form.tag.data, current_user.get_id())
        if mark_sum == -1:
            return render_template('mark.html', title='mark', form=form, marks=mark, mark_sum=mark_sum, weight_sum=weight_sum)
        weight, weight_sum = controller.get_question_mark(form.tag.data)
        mark=zip(mark,weight)
    return render_template('mark.html', title='mark',form=form,marks=mark,mark_sum=mark_sum,weight_sum=weight_sum)


@app.route('/Upload_question', methods=['GET', 'POST'])
@login_required
def Upload_question():
    if current_user.if_adm()!=1:
        return redirect(url_for('welcome'))
    form = QuestionForm()
    if form.validate_on_submit():
        tag=form.Tag.data
        mark=form.Mark.data
        que=form.Que.data
        stand_answer=form.Stand_answer.data
        que=questions(tag=tag,mark=mark,content=que,stand_answer=stand_answer)
        db.session.add(que)
        db.session.commit()
        flash("Questions saved!")
    return render_template('Upload_question.html', title='Upload_question', form=form)


@app.route('/User_management', methods=['GET', 'POST'])
@login_required
def User_management():
    if current_user.if_adm() != 1:
        return redirect(url_for('welcome'))
    users = User.query.all()

    return render_template('User_management.html', title='User_management', Users_list=users)
    

@app.route('/delete/<user_id>')
@login_required
def delete_user(user_id):
    if current_user.if_adm() != 1:
        return redirect(url_for('welcome'))
    controller.delete_user(user_id)
    flash("User"+str(user_id)+ " has been deleted!")
    return redirect(url_for('User_management'))


@app.route('/make_admin/<user_id>')
@login_required
def make_admin(user_id):
    if current_user.if_adm() != 1:
        return redirect(url_for('welcome'))
    controller.make_admin(user_id)
    flash("User"+str(user_id)+ " now is admin!")
    return redirect(url_for('User_management'))


@app.route('/manual_check?tag=<tag>&user_id=<user_id>&index=<index>', methods=['GET', 'POST'])
@login_required
def manual_check(tag,user_id,index):
    if current_user.if_adm() != 1:
        return redirect(url_for('welcome'))
    
    index=int(index)
    form=MarkForm()
    ques, ids = controller.get_questions(tag)
    limit = len(ques)
    que = ques[index]
    que_id = ids[index]
    if index >= limit-1:
        limit = 0
    answers=controller.get_answer(que_id,user_id)
    if form.validate_on_submit():
        mark = form.Mark.data
        ans=answer.query.filter_by(question_id=que_id,user_id=user_id).first()
        ans.mark=mark
        db.session.commit()
        flash("mark has been uploaded")
    
    return render_template('manual_check.html', title='manual_check', form=form, question=que, answer=answers, nextindex=str(index+1), lastindex=str(index-1), limit=limit,user_id=user_id,tag=tag)


@app.route('/get_answer', methods=['GET', 'POST'])
@login_required
def get_answer():
    if current_user.if_adm() != 1:
        return redirect(url_for('welcome'))
    
    user_selector = []
    userlist = User.query.all()
    for user in userlist:
        user_selector.append((user.get_id(), user.get_user_name()))

    class UserTagForm(FlaskForm):
        pass 
    setattr(UserTagForm, 'tag', SelectField(choices=controller.get_tags()))
    setattr(UserTagForm, 'user', SelectField(choices=user_selector))
    setattr(UserTagForm, 'submit', SubmitField('Get answer'))
    form = UserTagForm()

    if form.is_submitted():
        tag=form.tag.data
        user=form.user.data
        return redirect(url_for('manual_check',user_id=user,tag=tag,index='0'))
        

    return render_template('get_answer.html', title='get_answer', form=form)


@app.route('/manage_que', methods=['GET', 'POST'])
@login_required
def manage_que():
    if current_user.if_adm() != 1:
        return redirect(url_for('welcome'))
    quelist = questions.query.all()
    return render_template('manage_que.html', title='Manage questions',que_list=quelist)


@app.route('/delete_que?que_id=<que_id>', methods=['GET', 'POST'])
@login_required 
def delete_que(que_id):
    if current_user.if_adm() != 1:
        return redirect(url_for('welcome'))
    mod = questions.query.filter_by(id=que_id).first()
    db.session.delete(mod)
    db.session.commit()
    flash("Question"+str(que_id) + " has been deleted!")
    return redirect(url_for('manage_que'))


@app.route('/ending', methods=['GET', 'POST'])
@login_required
def ending():
    return render_template('endingpage.html', title='End_quiz')
