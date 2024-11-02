from flask_wtf import FlaskForm
from flask import current_app as app
from wtforms import (StringField, PasswordField,
                     SubmitField, SelectField,
                     TextAreaField, IntegerField,
                     FileField, DecimalField)
from wtforms.validators import DataRequired, Email, EqualTo , Regexp, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired


title_choices = [("mr", 'mr'),
                 ("miss", 'miss'),
                 ("mrs", 'mrs'),
                 ("dr", 'dr'),
                 ("prof", 'prof')]

class RegisterForm(FlaskForm):

    email = StringField(label='Email:', validators=[DataRequired(), Email()])
    first_name = StringField(label='First Name',validators=[DataRequired()])
    last_name = StringField(label='Last Name',validators=[DataRequired()])
    school = StringField(label='School',validators=[DataRequired()])
    title = SelectField("Title", choices=title_choices,
                        validators=[DataRequired()])
   
    submit = SubmitField('Add user')

class RequestRegisterForm(FlaskForm):

    email = StringField(label='Email:', validators=[DataRequired(), Email()])
    first_name = StringField(label='First Name',validators=[DataRequired()])
    last_name = StringField(label='Last Name',validators=[DataRequired()])
    school = StringField(label='School',validators=[DataRequired()])
    title = SelectField("Title", choices=title_choices,
                        validators=[DataRequired()])
    
   
    submit = SubmitField('Request Registration')


class LoginForm(FlaskForm):

    email = StringField(label='Email:', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


title_choices = [("mr", 'mr'),
                 ("miss", 'miss'),
                 ("mrs", 'mrs'),
                 ("dr", 'dr'),
                 ("prof", 'prof')]


class ProfileForm(FlaskForm):
    first_name = StringField(label="First Name", validators=[DataRequired()])
    last_name = StringField(label="Last Name", validators=[DataRequired()])
    title = SelectField("Title", choices=title_choices,
                        validators=[DataRequired()])
    photo = StringField(label='photo', validators=[DataRequired()])
    submit = SubmitField('update Profile', validators=[DataRequired()])

class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    

class UpdateProfileForm(FlaskForm):
    first_name = StringField(label='First Name', validators=[Regexp(r'^[a-zA-Z]+$', message="name  can only contain letters")])
    last_name = StringField(label='Last Name', validators=[Regexp(r'^[a-zA-Z]+$', message="name  can only contain letters")])
    photo_url = FileField('Profile Photo', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    title = SelectField(choices=title_choices)
    submit = SubmitField('Update Profile')