from flask import render_template, request, redirect, abort, current_app, session
from flask_login import current_user
from . import main
from .shortener import generate_short_url_code, validate_custom_short_code, generate_qr_code
from .safe_browsing import check_url_safety
from datetime import datetime, timezone
import validators

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        #get form values
        url = request.form.get("url")
        custom_short_code = request.form.get("customShortCode")
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


        url_data = {
            "short_url_code":   short_url_code,
            "original_url":     url,
            "created_at":       datetime.now(timezone.utc),
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

        #password protection
        if password:
            bcrypt = current_app.bcrypt
            url_data["password"] = bcrypt.generate_password_hash(password).decode("utf-8")
            #implement backend validation

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
        if url["password"]:
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

#debug testing route
@main.route("/my_urls")
def list_urls():
    urls = current_app.urls

    if current_user.is_authenticated:
        user_urls = list(urls.find({"user_id": current_user.get_id()}))
        print("user urls: ", user_urls)
    else:
        guest_url_codes = session.get("guest_url_codes", [])
        if guest_url_codes:
            guest_urls = list(urls.find({"short_url_code": {"$in": guest_url_codes}}))
            print("guest urls: ", guest_urls)
            session.pop("guest_url_codes", None)     #testing
        else:
            print("no guest codes")


    return render_template("index.html")