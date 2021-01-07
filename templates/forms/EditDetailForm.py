from wtforms import Form,PasswordField,validators,SelectField
from wtforms.fields.core import StringField

class EditDetailForm(Form):
    category = SelectField('Category', choices=[('username','Username'), ('email','Registration E-mail'), ('password','Password'), ('platform', 'Platform')])
    newPw = PasswordField("NEW PASSWORD", validators=[validators.DataRequired(message="Please, enter valid password.")])
    anyInfo = StringField("NEW")