from flask import Flask,render_template, redirect, url_for, session, request
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from templates.forms.LoginForm import LoginForm
from templates.forms.RegisterForm import RegisterForm
from templates.forms.PasswordForm import PasswordForm
from templates.forms.SecretKeyForm import SecretKeyForm
from templates.forms.EditProfileForm import EditProfileForm
from templates.forms.EditDetailForm import EditDetailForm
from passlib.handlers.sha2_crypt import sha256_crypt
from functools import wraps
from templates.includes.encryption import Encryption

app = Flask(__name__)
app.secret_key = "pwcase"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:asd123@localhost/pwcase' 
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
    crypto_key = db.Column(db.Text, nullable=False)
    password_list = db.relationship('Passwords', backref='users', lazy=True)

class Passwords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_mail = db.Column(db.String(80), nullable=False)
    platform_username = db.Column(db.String(80), nullable=False)
    platform_password = db.Column(db.Text, nullable=False)
    platform = db.Column(db.String(80), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Please login to view this page.", "danger")
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
                session["id"] = result.id
                session["crypto_key"] = result.crypto_key
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
        crypto_key = Encryption.createKey()
        new_user = Users(name_surname=name, username=username, secret_key=secret_key, crypto_key=crypto_key , email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("You have successfully registered !", "success")
        return redirect(url_for("login"))
    else:
        return render_template("pages/register.html", form=form)

# Dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    password_list = Passwords.query.filter_by(person_id=session["id"])
    pw_symbol = str("*")*8
    return render_template("pages/dashboard.html", pw_symbol=pw_symbol , password_list=password_list)

# Add Password
@app.route("/addpw", methods=["GET","POST"])
@login_required
def addPassword():
    form = PasswordForm(request.form)
    if request.method=="POST" and form.validate():
        email = form.registration.data
        username = form.username.data
        password = Encryption.encryptData(session["crypto_key"], form.password.data)
        platform = form.platform.data
        new_data = Passwords(registration_mail = email, platform_username = username, platform_password = password, platform=platform, person_id = session["id"])
        db.session.add(new_data)
        db.session.commit()
        flash("You have successfully added your data !", "success")
        return redirect(url_for("dashboard"))
    else:
        return render_template("pages/addpw.html",form=form)

# Delete Password
@app.route("/deletepw/<string:id>")
@login_required
def deletePassword(id):
    password = Passwords.query.filter_by(id=id).first()
    if password and password.person_id == session["id"]:
        flash("You have deleted information successfully","success")
        db.session.delete(password)
        db.session.commit()
        return redirect(url_for("dashboard"))
    else:
        flash("You do not have permission to delete this information!", "warning")
        return redirect(url_for("dashboard"))

# Edit Detail
@app.route("/edit/<string:id>", methods=["GET","POST"])
@login_required
def editDetail(id):
    """
        This function is just for redirect other section.
    """
    form = EditDetailForm(request.form)
    if request.method == "GET":
        return render_template("/pages/edit.html", form=form)
    else:
        choose = True
        section = form.category.data
        return redirect(url_for("editDetailSection", id=id ,section=section))

# Edit Password
@app.route("/edit/<string:id>/<string:section>", methods=["GET", "POST"])
@login_required
def editDetailSection(id, section):
    form = EditDetailForm(request.form)
    if request.method == "GET":
            choose = True
            if section == "password":
                return render_template("pages/edit.html", form=form, choose=choose, pw=True)
            else:
                return render_template("pages/edit.html", form=form, choose=choose)
    else:
        passwordDetail = Passwords.query.filter_by(id=id).first()
        if passwordDetail:
            if section == "password":
                passwordDetail.platform_password = Encryption.encryptData(form.newPw.data)
                db.session.commit()
                flash("Your details has changed successfully !", "success")
                return redirect(url_for("dashboard"))
            elif section == "username":
                passwordDetail.platform_username = form.anyInfo.data
                db.session.commit()
                flash("Your details has changed successfully !", "success")
                return redirect(url_for("dashboard"))
            elif section == "email":
                passwordDetail.registration_mail = form.anyInfo.data
                db.session.commit()
                flash("Your details has changed successfully !", "success")
                return redirect(url_for("dashboard"))
            elif section == "platform":
                passwordDetail.platform = form.anyInfo.data
                db.session.commit()
                flash("Your details has changed successfully !", "success")
                return redirect(url_for("dashboard"))
        else:
            flash("There is no information for this ID !", "warning")
            return redirect(url_for("dashboard"))

# Show Password
@app.route("/detail/<string:id>", methods=["GET","POST"])
@login_required
def showDetail(id):
    form = SecretKeyForm(request.form)
    if request.method == "GET":
        return render_template("pages/detail.html", form=form)
    else:
        secret_key = form.secret_key.data
        user = Users.query.filter_by(id=session["id"]).first()
        if secret_key == str(user.secret_key):
            password = Passwords.query.filter_by(id=id).first()
            if password and password.person_id == session["id"]:
                password.platform_password = Encryption.decryptData(session["crypto_key"], password.platform_password)
                auth = True
                flash("You have entered correct secret key ! Here is your information...", "success")
                return render_template("pages/detail.html", auth=auth, pw=password, form=form)
            else:
                flash("There is no data for you with this ID!", "danger")
                auth=False
                return render_template("pages/detail.html", auth=auth, form=form)
        else:
            auth= False
            flash("You have entered wrong secret key !", "danger")
            return render_template("pages/detail.html", auth=auth, form=form)

# Show Profile
@app.route("/profile")
@login_required
def profile():
    user = Users.query.filter_by(id=session["id"]).first()
    return render_template("/pages/profile.html", user=user)

# Edit Profile
@app.route("/editprofile", methods=["GET","POST"])
@login_required
def editProfile():
    """
        This function is just for redirect other section.
    """
    form = EditProfileForm(request.form)
    if request.method == "GET":
        return render_template("/pages/editprofile.html", form=form)
    else:
        choose = True
        section = form.category.data
        return redirect(url_for("editProfileSection", section=section))

@app.route("/editprofile/<string:section>", methods=["GET","POST"])
@login_required
def editProfileSection(section):
    form = EditProfileForm(request.form)
    if request.method == "GET":
        choose = True
        if section == "password":
            return render_template("pages/editprofile.html", form=form, choose=choose, pw=True)
        else:
            return render_template("pages/editprofile.html", form=form, choose=choose)
    else:
        user = Users.query.filter_by(id=session["id"]).first()
        if section == "password":
            user.password == sha256_crypt.encrypt(form.newPw.data)
            db.session.commit()
            flash("Your password has been changed successfully! Please login again!", "warning")
            return redirect(url_for("logout"))
        elif section == "username":
            user.username = form.anyInfo.data
            db.session.commit()
            flash("Your information has been changed successfully!", "success")
            return redirect(url_for("logout"))
        elif section == "email":
            user.email = form.anyInfo.data
            db.session.commit()
            flash("Your information has been changed successfully!", "success")
            return redirect(url_for("profile"))
        elif section == "secret_key":
            user.secret_key = form.anyInfo.data
            db.session.commit()
            flash("Your information has been changed successfully!", "success")
            return redirect(url_for("profile"))
        elif section == "name":
            user.name_surname = form.anyInfo.data
            db.session.commit()
            flash("Your information has been changed successfully!", "success")
            return redirect(url_for("profile"))

################################################################################################################

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)