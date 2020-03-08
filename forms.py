from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, TimeField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Unique
from model import User


class Register(FlaskForm):
    """Registration Form"""
    # validators import (from wtforms.validators) !
    user_name = StringField('Username', validators=[DataRequired(), Unique(), Length(min=4, max=35)])
    # import email validators (from wtforms.validators)
    email = StringField('Email', validators=[DataRequired(), Email(), Unique()])
    # import Password validator (from wtforms)
    password = PasswordField('Password', validators=[DataRequired()])
    # needs to match password using equalto validator (from wtforms.validators)
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Join')

    def check_username(self, user_name):
        user = User.query.filter_by(user_name=user_name.data).one()
        if user:
            raise ValidationError('Username already exists. Please choose another user name.')
    
    def check_email(self, email):
        user = User.query.filter_by(email=email.data).one()
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

    dive_name = StringField('Dumpster Business', validators=[DataRequired(), Length(max=200)])
    # dive_location = how to implement google api to default to current location.
    dive_day = SelectField('Dive Day', validators=[DataRequired()],
                            choices=[('Sunday', 0),
                                     ('Monday', 1), 
                                     ('Tuesday', 2), 
                                     ('Wednesday', 3), 
                                     ('Thursday', 4), 
                                     ('Friday', 5), 
                                     ('Saturday', 6)])
    dive_date = DateField('Dive Date', format='%m/%d/%Y')
    dive_time = TimeField('Dive Time', validators=[DataRequired()])
    rating = RadioField('Dive Rating', default=3, 
                        choices=[(0, 'Worst'),
                                 (1, 'Bad'),
                                 (2, 'Poor'),
                                 (3, 'Meh'),
                                 (4, 'Beneficial'),
                                 (5, 'Best')])
    safety = BooleanField('Safe Dive?')
    items = StringField('What did you find?', validators=[Length(max=300)])
    submit = SubmitField('Add Dive')
