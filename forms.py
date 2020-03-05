from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, TimeField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class Register(FlaskForm):
    """Registration Form"""
    # validators import (from wtforms.validators) !
    user_name = StringField('Username', validators=[DataRequired(), Length(min=4, max=35)])
    # import email validators (from wtforms.validators)
    email = StringField('Email', validators=[DataRequired(), Email()])
    # import Password validator (from wtforms)
    password = PasswordField('Password', validators=[DataRequired()])
    # needs to match password using equalto validator (from wtforms.validators)
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Join the Dive')


class Login(FlaskForm):
    """Login Form"""
    user_name = StringField('Username', validators=[DataRequired(), Length(min=4, max=35)])
    password = PasswordField('Password', validators=[DataRequired()])
    # create a remember me checkbox (bool) by importing BooleanField from wtforms
    remember = BooleanField('Remember me')
    submit = SubmitField('Go Glean')

class Review(FlaskForm):
    """Dive Review"""

    dive_day = SelectField('Dive Day', validators=[DataRequired()],
                            choices=[('Sunday', 0),
                                     ('Monday', 1), 
                                     ('Tuesday', 2), 
                                     ('Wednesday', 3), 
                                     ('Thursday', 4), 
                                     ('Friday', 5), 
                                     ('Saturday', 6)])
    dive_date = DateField('Dive Date', format='%m/%d/%Y')
    dive_time = TimeField('Dive Time', validators=[DataRequired()])# Set default to utcnow but time only.
    rating = RadioField('Dive Rating', default=3, choices=[(0, 'Worst'),
                                                           (1, 'Bad'),
                                                           (2, 'Poor'),
                                                           (3, 'Meh'),
                                                           (4, 'Beneficial'),
                                                           (5, 'Best')])
    safety = BooleanField('Safe Dive?')
    items = StringField('What did you find?', validators=[Length(max=300)])
