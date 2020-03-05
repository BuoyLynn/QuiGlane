from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
