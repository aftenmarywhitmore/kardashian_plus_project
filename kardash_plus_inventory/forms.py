from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email



class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()]) 
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    password = PasswordField('Password', validators = [DataRequired()]) 
    submit_button = SubmitField() 



#Email, Password, and Submit Button all on this page 
#Make sure Flask-WTF is pip installed
#Import FlaskForm
#Import StringField, PasswordField, SubmitField (aka email, password, and submit button)