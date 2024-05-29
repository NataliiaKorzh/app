from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from models import Group


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class TicketForm(FlaskForm):
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('In review', 'In review'), ('Closed', 'Closed')])
    note = TextAreaField('Note', validators=[DataRequired()])
    group = SelectField('Group', coerce=int, choices=[(group.id, group.name) for group in Group.query.all()])
    submit = SubmitField('Submit')
