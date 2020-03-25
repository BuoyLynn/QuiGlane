from datetime import datetime, date, time
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, TimeField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, Email, EqualTo, ValidationError
from model import User, Site, Dive


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

    dive_name = StringField('Dumpster Owner', validators=[DataRequired(), Length(max=200)],render_kw={"placeholder": "Associated Business Name"})
    dive_address = StringField('Address', validators=[Optional()])
    dive_day = SelectField('Dive Day', validators=[DataRequired()],
                            choices=[(0, 'Sunday'),
                                     (1, 'Monday'), 
                                     (2, 'Tuesday'), 
                                     (3, 'Wednesday'), 
                                     (4, 'Thursday'), 
                                     (5, 'Friday'), 
                                     (6, 'Saturday')])
    dive_date = DateField('Dive Date', validators=[Optional()], format='%m/%d/%Y', render_kw={"type": "date"})
    dive_time = TimeField('Dive Time', default=datetime.now(), validators=[DataRequired()])
    rating = SelectField('Dive Rating', default=3, validators=[DataRequired()],
                        choices=[(0, 'Worst'),
                                 (1, 'Bad'),
                                 (2, 'Poor'),
                                 (3, 'Meh'),
                                 (4, 'Good'),
                                 (5, 'Excellent')])
    safety = BooleanField('Safe Dive?', default="checked", validators=[Optional()])
    items = TextAreaField('What did you find?', validators=[Optional(), Length(max=300)], render_kw={"placeholder": "Eg. fresh cabbage, firm potatoes, squashed tomatoes, bread baked today and more!"})
    submit = SubmitField('Add Dive')
