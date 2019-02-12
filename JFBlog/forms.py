import re

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    TextField,
    TextAreaField,
    PasswordField,
    BooleanField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, EqualTo, URL
from .models import User


class RegisterForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=191)])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm Password', [
                            DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('User with name already exist.')
            return False
        return True


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=191)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember Me')

    def validate(self):
        """Validator for check the account information."""
        check_validata = super(LoginForm, self).validate()

        if not check_validata:
            return False

        # Check the user whether exist.
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password.')
            return False

        # Check the password whether right.
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password.')
            return False

        return True


def custom_email(form_object, filed_object):
    """Define a validator"""

    if not re.match(r"[^@+@[&@]+\.[^@]]+", filed_object.data):
        raise ValidationError('Field must be a valid email address.')


class CommentForm(FlaskForm):
    """Form validator for comment."""

    # et filed(InputBox) for enter the data.
    # patam validators: setup list of validators
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=191)]
    )

    text = TextField('Comment', validators=[DataRequired()])


class PostForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(max=191)])
    text = TextAreaField('Blog Content', [DataRequired()])
