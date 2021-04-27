from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired
 

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

def SearchForm(FlaskForm):
    model = TextField('Models', validators=[InputRequired()])
    make = TextField('Models', validators=[InputRequired()])
    

class AddNewCarForm(FlaskForm):
    make = StringField("Make of Car", validators = [DataRequired()])
    model = TextAreaField("Model of Car", validators = [DataRequired()])
    
    colour = StringField("Colour of Car", validators = [DataRequired()])

    year = TextAreaField("Year", validators = [DataRequired()])

    price = StringField("Price", validators = [DataRequired()])

    cartype = SelectField("Car Type", choices = [("suv", "SUV"), ("sedan","Sedan")])

    transmission = StringField("Transmission", choices = [("automatic", "Automatic"), ("manual","Manual")])
    
    description = StringField("Description", validators = [DataRequired()])
    
    photo = FileField("Photo", validators = [FileRequired(),FileAllowed(["jpg","png","jpeg", "Images Only!"])])