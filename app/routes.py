from flask import render_template, flash, request, redirect
from app import app
from app.LoginForm import LoginForm

# app = Flask(__name__)
app.secret_key = 'SECRET KEY'
@app.route('/')
@app.route('/index')
def index():
    return render_template('Application.html')

@app.route('/canLogin', methods = ['POST','GET'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        username = request.form.get("username")
        flash(username)


    return render_template('Can_log.html', form = form)

@app.route('/adminLogin', methods = ['GET','POST'])
def adminLogin():
    form = LoginForm()
    return render_template('Admin_log.html')