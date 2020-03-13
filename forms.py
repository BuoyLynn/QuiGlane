from datetime import datetime, date, time
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, TimeField, RadioField
from wtforms.validators import DataRequired, Optional, Length, Email, EqualTo, ValidationError
from model import User


class Register(FlaskForm):
    """Registration Form"""
    # validators import (from wtforms.validators) !
    user_name = StringField('Username', validators=[DataRequired(), Length(min=4, max=35)])
    # import email validators (from wtforms.validators)
    email = StringField('Email', validators=[DataRequired(), Email(message=("Not valid."))])
    # import Password validator (from wtforms)
    password = PasswordField('Password', validators=[DataRequired()])
    # needs to match password using equalto validator (from wtforms.validators)
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    twitter = StringField('Twitter', validators=[Optional()])

    submit = SubmitField('Join')

    def check_username(self, user_name):
        user = User.query.filter_by(user_name=user_name.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose another user name.')
    
    def check_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already in use.')


class Login(FlaskForm):
    """Login Form"""
    user_name = StringField('Username', validators=[DataRequired(), Length(min=4, max=35)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Go Glean')


class Review(FlaskForm):
    """Dive Review"""

    dive_name = StringField('Dumpster Owner (Business Name)', validators=[DataRequired(), Length(max=200)])
    dive_address = StringField('Address', validators=[Optional()])
    dive_day = SelectField('Dive Day', validators=[DataRequired()],
                            choices=[('Sunday', 0),
                                     ('Monday', 1), 
                                     ('Tuesday', 2), 
                                     ('Wednesday', 3), 
                                     ('Thursday', 4), 
                                     ('Friday', 5), 
                                     ('Saturday', 6)])
    dive_date = DateField('Dive Date', validators=[Optional()], format='%m/%d/%Y')
    dive_time = TimeField('Dive Time', default=datetime.now(), validators=[DataRequired()])
    rating = RadioField('Dive Rating', default=3, validators=[DataRequired()],
                        choices=[(0, 'Worst'),
                                 (1, 'Bad'),
                                 (2, 'Poor'),
                                 (3, 'Meh'),
                                 (4, 'Good'),
                                 (5, 'Excellent')])
    safety = BooleanField('Safe Dive?', validators=[DataRequired()])
    items = StringField('What did you find?', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Add Dive')
