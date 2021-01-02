from wtforms import Form,StringField,TextAreaField,PasswordField, form,validators
from wtforms.fields.core import IntegerField

class PasswordForm(Form):
    registration = StringField("EMAIL", validators=[validators.Email(message = "Please enter valid email !"), validators.DataRequired()])
    username = StringField("USERNAME", validators=[validators.Length(min=5, max=35), validators.DataRequired()])
    password = PasswordField("PASSWORD", validators=[validators.DataRequired(message="Please, enter valid password.")])
    platform = StringField("WHICH PLATFORM?", validators=[validators.Length(min=3, max=40), validators.DataRequired(message="Please enter platform name.")])