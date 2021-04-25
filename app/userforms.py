from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Email
 

class RegisterForm(FlaskForm):
    username=StringField('Username', validators=[InputRequired()])
    password=StringField('Password', validators=[InputRequired()])
    name=StringField('Full Name', validators=[InputRequired()])
    email=StringField('Email', validators=[InputRequired(), Email()])
    location=StringField('Location', validators=[InputRequired()])
    biography=TextAreaField('Biography', validators=[InputRequired()])
    photo=FileField('Upload Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])

class LoginForm(FlaskForm):
    username=StringField('Username', validators=[InputRequired()])
    password=PasswordField('Password', validators=[InputRequired()])
