from flask import render_template, request, redirect, abort, url_for
from flask_login import login_required, login_user, logout_user
from app import app, urls, users, bcrypt
from .shortener import generate_short_url_code, validate_custom_short_code, generate_qr_code
from .safe_browsing import check_url_safety
from .models import User
import validators


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")   #get string from form
        custom_short_code = request.form.get("customShortCode")

        #validate URL here
        if not (url.startswith("http://") or url.startswith(("https://"))):
            url = "http://" + url

        if not (validators.url(url)):
            return render_template("index.html", error_message="Invalid URL provided.")

        #google safe browsing
        safe, error_message = check_url_safety(url)
        if not safe:
            return render_template("index.html", error_message=error_message)

        #custom short code
        if custom_short_code:
            #validation
            valid, error_message = validate_custom_short_code(custom_short_code)
            if not valid:
                return render_template("index.html", error_message=error_message)
            short_url_code = custom_short_code
        else:
            #no custom short code -> generate code
            short_url_code = generate_short_url_code()

        #insert to database
        urls.insert_one({
            "short_url_code":   short_url_code,
            "original_url":     url
        })

        short_url = request.host_url + short_url_code    #domain + code
        qr = generate_qr_code(short_url)

        return render_template("index.html", short_url=short_url, qr_code_image=qr)

    return render_template("index.html")

@app.route("/<short_url_code>")
def redirect_url(short_url_code):
    url = urls.find_one({"short_url_code": short_url_code});
    if url:
        return redirect(url["original_url"])
    else:
        return abort(404)   #temporary error message for short url not found



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        #may move validation and adding to seperate py script
        username_exists = users.find_one({"username": username})
        if username_exists:
            return "user already exists"        #temporary

        if password != confirm_password:
            return "passwords do not match"     #temporary

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
            return redirect(url_for("index"))   #temporary redirect
        else:
            print("error finding user data")    #debug

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_data = users.find_one({"username": username})

        if user_data and bcrypt.check_password_hash(user_data["password"], password):
            user = User(username=user_data["username"])
            login_user(user)
            return redirect(url_for("index"))
        else:
            print("invalid/error")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    #inform user
    return redirect(url_for("index"))