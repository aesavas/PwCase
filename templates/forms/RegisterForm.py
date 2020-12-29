from wtforms import Form,StringField,TextAreaField,PasswordField, form,validators
from wtforms.fields.core import IntegerField

class RegisterForm(Form):
    name = StringField("NAME and SURNAME", validators=[validators.Length(min=5, max=30)])
    username = StringField("USERNAME", validators=[validators.Length(min=5, max=35)])
    email = StringField("EMAIL", validators=[validators.Email(message = "Please enter valid email !")])
    secret_key = IntegerField("SECRET KEY", validators=[validators.Length(min=4, max=8)])
    password = PasswordField("PASSWORD", validators=[
        validators.DataRequired(message="Please, enter valid password."),
        validators.EqualTo(fieldname="re_password", message="Passwords do not match!")
    ])
    re_password = PasswordField("RE-ENTER PASSWORD")