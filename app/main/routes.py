from flask import render_template, request, redirect, abort, current_app, session
from flask_login import current_user
from . import main
from .shortener import generate_short_url_code, validate_custom_short_code, generate_qr_code, get_users_urls
from .safe_browsing import check_url_safety
from datetime import datetime, timezone, timedelta
import validators

DEFAULT_EXPIRATION = 30

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        #get form values
        url = request.form.get("url")
        custom_short_code = request.form.get("customShortCode")
        expiration_date = request.form.get("expirationDate")
        timezone_offset = request.form.get("timezoneOffset")
        click_limit = request.form.get("clickLimit")
        password = request.form.get("password")

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

        #URL expiration
        if expiration_date:
            expiration_date = datetime.fromisoformat(expiration_date)
            if timezone_offset:
                expiration_date = expiration_date - timedelta(minutes=int(timezone_offset))
            expiration_date = expiration_date.astimezone(timezone.utc)
        else:
            expiration_date = datetime.now(timezone.utc) + timedelta(DEFAULT_EXPIRATION)

        #create url data
        url_data = {
            "short_url_code":   short_url_code,
            "original_url":     url,
            "created_at":       datetime.now(timezone.utc),
            "expiration_date":  expiration_date,
            "last_accessed":    None,
            "click_count":      0
        }

        #user id/guest
        if current_user.is_authenticated:
            url_data["user_id"] = current_user.get_id()
        else:
            if "guest_url_codes" not in session:
                session["guest_url_codes"] = []
            session["guest_url_codes"].append(short_url_code)
            session.modified = True

        #click limit
        if click_limit:
            if click_limit.isdigit():
                url_data["click_limit"] = int(click_limit)
            else:
                return render_template("index.html", error_message="Click limit must be an integer.")

        #password protection
        if password:
            bcrypt = current_app.bcrypt
            #implement backend validation
            url_data["password"] = bcrypt.generate_password_hash(password).decode("utf-8")

        #insert to database
        urls = current_app.urls
        urls.insert_one(url_data)

        short_url = request.host_url + short_url_code    #domain + code
        qr = generate_qr_code(short_url)

        return render_template("index.html", short_url=short_url, qr_code_image=qr)

    return render_template("index.html")

@main.route("/<short_url_code>", methods=["GET", "POST"])
def redirect_url(short_url_code):
    urls = current_app.urls
    url = urls.find_one({"short_url_code": short_url_code})

    if url:
        #check if the url has expired
        #convert to timeaware datetime
        if url["expiration_date"].tzinfo is None:
            url["expiration_date"] = url["expiration_date"].replace(tzinfo=timezone.utc)

        if url["expiration_date"] < datetime.now(timezone.utc) or ("click_limit" in url and url["click_count"] >= url["click_limit"]):
            urls.delete_one({"short_url_code": short_url_code})
            return abort(404)   #temporary error message for short url not found


        #check if there the url is password protected
        if "password" in url and url["password"]:
            if request.method == "POST":
                password = request.form.get("password")
                bcrypt = current_app.bcrypt
                if bcrypt.check_password_hash(url["password"], password):
                    urls.update_one(
                        {"short_url_code": short_url_code},
                        {"$inc": {"click_count": 1},                                    #increment click count by 1
                         "$set": {"last_accessed": datetime.now(timezone.utc)}},        #set last accessed time to now
                    )
                    return redirect(url["original_url"])
                else:
                    return render_template("protected_redirect.html", error_message="Incorrect password.")
            return render_template("protected_redirect.html")       #get request
        else:
            urls.update_one(
                {"short_url_code": short_url_code},
                {"$inc": {"click_count": 1},                                    #increment click count by 1
                 "$set": {"last_accessed": datetime.now(timezone.utc)}},        #set last accessed time to now
            )
            return redirect(url["original_url"])
    else:
        return abort(404)   #temporary error message for short url not found

@main.route("/dashboard")
def dashboard():
    user_urls = get_users_urls()
    return render_template("dashboard.html", user_urls=user_urls)

@main.route("/about")
def about():
    return render_template("about.html")