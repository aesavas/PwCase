from flask import Flask,render_template, redirect, url_for, session, logging, request
from flask.helpers import flash
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField, form,validators
from passlib.handlers.sha2_crypt import sha256_crypt

app = Flask(__name__)
app.secret_key = "pwcase"

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)