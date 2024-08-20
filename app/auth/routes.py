from flask import render_template, request, redirect, url_for, current_app
from flask_login import login_required, login_user, logout_user
from . import auth
from .models import User
#create a validation file


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        #may move validation and adding to seperate py script
        users = current_app.users
        username_exists = users.find_one({"username": username})
        if username_exists:
            return "user already exists"        #temporary

        if password != confirm_password:
            return "passwords do not match"     #temporary

        bcrypt = current_app.bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        users.insert_one({
            "username": username,
            "password": hashed_password})

        #temporary testing
        print("signed up")
        user_data = users.find_one({"username": username})
        if user_data:
            user = User(username=user_data["username"])
            login_user(user)
            return redirect(url_for("main.index"))   #temporary redirect
        else:
            print("error finding user data")    #debug

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        users = current_app.users
        user_data = users.find_one({"username": username})

        bcrypt = current_app.bcrypt
        if user_data and bcrypt.check_password_hash(user_data["password"], password):
            user = User(username=user_data["username"])
            login_user(user)
            return redirect(url_for("main.index"))
        else:
            print("invalid/error")

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    #inform user
    return redirect(url_for("main.index"))