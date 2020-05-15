from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,InputRequired
from app.models import User
from app import controller


class LoginForm(FlaskForm):

    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class AnswerForm(FlaskForm):
    answer = TextAreaField('answer', validators=[DataRequired()])
    submit = SubmitField('Save')

# class TagForm(FlaskForm):
#     tag = SelectField(validators=[DataRequired('Please select a tag')], choices=controller.get_tags())
#     submit = SubmitField('get quiz')

class QuestionForm( FlaskForm ):
    Tag = StringField('Tag', validators=[DataRequired()])
    Mark = IntegerField('Mark', validators=[DataRequired()])
    Que = TextAreaField('Question', validators=[DataRequired()])
    Stand_answer = TextAreaField('Stand_answer')
    submit = SubmitField('Submit')

class MarkForm( FlaskForm ):
    Mark = IntegerField('Mark', validators=[InputRequired()])
    submit = SubmitField('Submit')

