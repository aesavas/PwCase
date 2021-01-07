from wtforms import Form,PasswordField,validators,SelectField
from wtforms.fields.core import StringField

class EditProfileForm(Form):
    category = SelectField('Category', choices=[('username','Username'), ('name','Name and Surname'), ('email','E-mail'),('secret_key','Secret Key'), ('password','Password')])
    newPw = PasswordField("NEW PASSWORD", validators=[validators.DataRequired(message="Please, enter valid password.")])
    anyInfo = StringField("NEW")