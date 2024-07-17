from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, FileField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from flask_wtf.file import FileAllowed
from flask_blog.models import User
# Converts python created to html forms automatically
class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(), Length(min=2 , max=20)])
    email=StringField('Email',validators=[DataRequired(),Email(), Length(max=120)])

    # def validate_email(self, email):
    #     try:
    #         valid = validate_email(email.data)
    #     except EmailNotValidError as e:
    #         raise ValidationError(str(e))

    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Sign Up')
    # checks if user attempts to use the same username for registration
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username is already taken! Please choose other username')

    # checks if user attempts to use the same email for registration
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email is already taken! Please choose other email')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(), Length(min=2 , max=20)])
    email=StringField('Email',validators=[DataRequired(),Email(), Length(max=120)])
    picture = FileField('Update Profile Picture\n', validators=[FileAllowed(['jpg','jpeg','png'])])
    submit=SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The username is already taken! Please choose other username')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The email is already taken! Please choose other email')

# form to request the password reset
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account for that email. You must register first!')

# Form to reset the password
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')