from flask import Flask, render_template, redirect, session, flash, request
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users/new", methods=["POST"])
def new_user():
    if User.validate_registration(request.form):
        user = {}
        for key in request.form:
            user[key] = request.form[key]
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        user["password"] = pw_hash
        new_id = User.register_user(user)
        session["user_id"] = new_id
        session["user_name"] = request.form["first_name"] + " " + request.form["last_name"]
        session["logged_in"] = True
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/users/login", methods=["POST"])
def login_user():
    login_info = request.form
    if User.validate_login(login_info):
        this_user = User.find_by_email(login_info)
        session["user_id"] = this_user.id
        session["user_name"] = this_user.first_name + " " + this_user.last_name
        session["logged_in"] = True
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/logout", methods=["POST"])
def logout():
    session["user_id"] = None
    session["user_name"] = None
    session["logged_in"] = False
    return redirect("/")

