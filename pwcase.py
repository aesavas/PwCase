from flask import Flask,render_template, redirect, url_for, session, logging, request
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from templates.forms.LoginForm import LoginForm
from templates.forms.RegisterForm import RegisterForm
from passlib.handlers.sha2_crypt import sha256_crypt

app = Flask(__name__)
app.secret_key = "pwcase"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:asd123@localhost/NEWDATABASENAME' # Buraya yeni databasein adi yazilacak.
db = SQLAlchemy(app)

# DB modelleri eklenecek!

#Index
@app.route("/")
def index():
    return render_template("index.html")


# Login
@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    return render_template("pages/login.html", form=form)

# Register
@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    return render_template("pages/register.html", form=form)




################################################################################################################

if __name__ == "__main__":
    app.run(debug=True)