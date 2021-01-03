from wtforms import Form,PasswordField,validators

class SecretKeyForm(Form):
    secret_key = PasswordField("SECRET KEY", validators=[validators.DataRequired(message="Please, enter valid password.")])