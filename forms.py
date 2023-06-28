from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SelectField, SubmitField, validators, PasswordField


class CafeForm(FlaskForm):
    name = StringField('Name of the caffe', validators=[DataRequired()], description='What is this caffe called?')
    chargers = SelectField('Quality and quantity of electric ports', validators=[DataRequired()],
                           choices=['Horrible', 'Bad', 'Average', 'Good', 'Excellent'])
    wifi = SelectField('Quality of WiFi and Internet connection', validators=[DataRequired()],
                           choices=['Horrible', 'Bad', 'Average', 'Good', 'Excellent'])
    env = SelectField('General environment', validators=[DataRequired()],
                      choices=['⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'])
    serv_food = SelectField('Quality of service and food', validators=[DataRequired()],
                      choices=['⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'])
    price = StringField('Price for a small espresso', validators=[DataRequired()],
                        description='Price for a small black coffee. Ex.: 2.35$, 1.85€')
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Your email address', validators=[DataRequired()])
    password = PasswordField('Your password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('Your first name', validators=[DataRequired()])
    surname = StringField('Your last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Your username', validators=[DataRequired()])
    password = PasswordField('Create password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Login')

        