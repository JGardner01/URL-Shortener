from flask import render_template, request, redirect, url_for, current_app
from flask_login import login_required, login_user, logout_user
from . import auth
from .models import User
from .auth_validation import validate_new_username, validate_new_password
from .session_util import transfer_guest_urls

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #get form inputs
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        valid_username, error_message = validate_new_username(username)
        if not valid_username:
            return error_message    #temp

        valid_password, error_message = validate_new_password(password, confirm_password)
        if not valid_password:
            return error_message    #temp

        #username and passwords are both valid

        bcrypt = current_app.bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        users = current_app.users
        if valid_username and valid_password:   #ensure that the code definitly does not touch the db collection unless valid
            users.insert_one({
                "username": username,
                "password": hashed_password})

            print("signed up")        #temporary testing

        user_data = users.find_one({"username": username})
        if user_data:
            user = User(username=user_data["username"])
            login_user(user)

            transfer_guest_urls()

            return redirect(url_for("main.index"))   #temporary redirect - change to dashboard
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

            transfer_guest_urls()

            return redirect(url_for("main.index"))
        else:
            print("invalid/error")  #temp debug

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    #implement informing user
    return redirect(url_for("main.index"))