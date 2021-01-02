from flask import Flask,render_template, redirect, url_for, session, logging, request
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from templates.forms.LoginForm import LoginForm
from templates.forms.RegisterForm import RegisterForm
from templates.forms.PasswordForm import PasswordForm
from passlib.handlers.sha2_crypt import sha256_crypt
from functools import wraps

app = Flask(__name__)
app.secret_key = "pwcase"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:asd123@localhost/pwcase' # Buraya yeni databasein adi yazilacak.
db = SQLAlchemy(app)

##############################################################################################################

# DB Models
# User table model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    name_surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80))
    password = db.Column(db.Text, nullable=False)
    secret_key = db.Column(db.Integer, nullable=False)


# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayi goruntulemek icin lutfen giris yapin.", "danger")
            return redirect(url_for("login"))
    return decorated_function


###############################################################################################################
# PAGES

#Index
@app.route("/")
def index():
    return render_template("index.html")


# Login
@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        result = Users.query.filter_by(username=username).first()
        if result:
            realpw = result.password
            if sha256_crypt.verify(password, realpw):
                flash("You have successfully logged in !", "success")
                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("index"))
            else:
                flash("You entered your password incorrectly. Please try again.", "danger")
                return redirect(url_for("login"))
        else:
            flash("Wrong username or password, please try again.", "danger")
            return redirect(url_for("login"))
    return render_template("pages/login.html", form=form)

# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You have logout succesfully.", "primary")
    return redirect(url_for("index"))

# Register
@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        secret_key = form.secret_key.data
        password = sha256_crypt.encrypt(form.password.data)
        re_password = sha256_crypt.encrypt(form.re_password.data)
        new_user = Users(name_surname=name, username=username, secret_key=secret_key, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("You have successfully registered !", "success")
        return redirect(url_for("login"))
    else:
        flash("Something went wrong ! Please try again.", "warning")
        return render_template("pages/register.html", form=form)

# Dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("pages/dashboard.html")

@app.route("/addpw", methods=["GET","POST"])
@login_required
def addPassword():
    form = PasswordForm(request.form)
    return render_template("pages/addpw.html",form=form)


################################################################################################################

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)