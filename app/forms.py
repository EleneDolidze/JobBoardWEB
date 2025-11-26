from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed

#Registration Form
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

#Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

#Job Form (Add/Edit Job)
class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    short_desc = StringField('Short Description', validators=[DataRequired()])
    full_desc = TextAreaField('Full Description', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    salary = StringField('Salary')
    location = StringField('Location')
    category = SelectField('Category', choices=[('IT','IT'),('Design','Design'),('Finance','Finance'),('Marketing','Marketing'),('Healthcare','Healthcare'),('Education','Education')])
    submit = SubmitField('Post Job')

#Profile Form (User Info Update)
class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_image = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Profile')


