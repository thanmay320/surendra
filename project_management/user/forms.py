from flask_wtf import FlaskForm
from wtforms.validators import  DataRequired,Email,EqualTo
from wtforms import  StringField,PasswordField,SubmitField
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    user_mail = StringField('Email', validators=[DataRequired(), Email()])
    user_friend=StringField('Best Friend Name',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')
class LoginForm(FlaskForm):
    user_mail = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
class ForgotPasswordForm(FlaskForm):
    user_mail = StringField('Email', validators=[DataRequired(), Email()])
    friend_name = StringField('Friend Name', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')