from wtforms import Form,StringField,PasswordField

class LoginForm(Form):
    username = StringField("USERNAME")
    password = PasswordField("PASSWORD")