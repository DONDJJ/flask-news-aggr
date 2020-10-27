from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import validators
from app.models import User

class LoginForm(FlaskForm):
    username= StringField("Username(Email)", validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Submit!")

class RegistrationForm(FlaskForm):
    email = StringField("Username(Email)", validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField("Submit!")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise validators.ValidationError("Use a different email")
