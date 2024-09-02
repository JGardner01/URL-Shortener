from flask import render_template, request, redirect, abort, current_app, session, jsonify
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

@main.route("/dashboard", methods=["GET"])
def dashboard():
    user_urls = get_users_urls()
    return render_template("dashboard.html", user_urls=user_urls)

@main.route("/shorten", methods=["POST"])
def shorten_url():
    url = request.json.get("url")
    custom_short_code = request.json.get("customShortCode")
    expiration_date = request.json.get("expirationDate")
    timezone_offset = request.json.get("timezoneOffset")
    click_limit = request.json.get("clickLimit")
    password = request.json.get("password")

    if not shorten_url:
        return jsonify({"error": "Short URL code was not specified."}), 400

    #validate URL here
    if not (url.startswith("http://") or url.startswith(("https://"))):
        url = "http://" + url
    if not (validators.url(url)):
        return jsonify({"error": "Invalid URL provided."}), 400

    #google safe browsing
    safe, error_message = check_url_safety(url)
    if not safe:
        return jsonify({"error": error_message}), 400

    #custom short code
    if custom_short_code:
        #validation
        valid, error_message = validate_custom_short_code(custom_short_code)
        if not valid:
            return jsonify({"error": error_message}), 400
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
            return jsonify({"error": "Click limit must be an integer."}), 400

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

    return jsonify({"success": True}), 200

@main.route("/edit", methods=["POST"])
def edit_url():
    short_url_code = request.json.get("shortURLCode")
    custom_short_code = request.json.get("customURLCode")
    new_expiration_date = request.json.get("newExpirationDate")
    timezone_offset = request.json.get("timezoneOffset")
    new_click_limit = request.json.get("newClickLimit")
    new_password = request.json.get("newPassword")

    if not short_url_code:
        return jsonify({"error": "Short URL code was not specified."}), 400

    urls = current_app.urls
    url = urls.find_one({"short_url_code": short_url_code})

    if url:
        edited_data = {}

        if custom_short_code:
            valid, error_message = validate_custom_short_code(custom_short_code)
            if not valid:
                return jsonify({"error": error_message}), 400
            else:
                edited_data["short_url_code"] = custom_short_code

        if new_expiration_date:
            new_expiration_date = datetime.fromisoformat(new_expiration_date)
            if timezone_offset:
                new_expiration_date = new_expiration_date - timedelta(minutes=int(timezone_offset))
            new_expiration_date = new_expiration_date.astimezone(timezone.utc)
            edited_data["expiration_date"] = new_expiration_date

        if new_click_limit:
            if new_click_limit.isdigit():
                edited_data["click_limit"] = int(new_click_limit)
            else:
                return jsonify({"error": "Click limit must be an integer."}), 400

        if new_password:
            bcrypt = current_app.bcrypt
            edited_data["password"] = bcrypt.generate_password_hash(new_password).decode("utf-8")

        if current_user.is_authenticated:
            if url["user_id"] == current_user.get_id():
                edited = urls.update_one({"short_url_code": short_url_code}, {"$set": edited_data})
                if edited.modified_count > 0:
                    return jsonify({"success": True}), 200
                else:
                    return jsonify({"error": "Error occurred while updating the shortened URL."}), 500
            else:
                return jsonify({"error": "Unauthorised"}), 403
        else:
            guest_url_codes = session.get("guest_url_codes", [])
            if short_url_code in guest_url_codes:
                edited = urls.update_one({"short_url_code": short_url_code}, {"$set": edited_data})
                if edited.modified_count > 0:
                    if custom_short_code:
                        guest_url_codes.remove(short_url_code)
                        guest_url_codes.append(custom_short_code)
                        session["guest_url_codes"] = guest_url_codes
                        session.modified = True
                    return jsonify({"success": True}), 200
                else:
                    return jsonify({"error": "Error occurred while updating the shortened URL."}), 500
            else:
                return jsonify({"error": "Unauthorised"}), 403
    else:
        return jsonify({"error": "Shortened URL not found"}), 404

@main.route("/delete", methods=["POST"])
def delete_url():
    short_url_code = request.json.get("short_url_code")
    if not short_url_code:
        return ({"error": "Short URL code was not specified."}), 400

    urls = current_app.urls
    url = urls.find_one({"short_url_code": short_url_code})

    if url:
        if current_user.is_authenticated:
            if url["user_id"] == current_user.get_id():
                deleted = urls.delete_one({"short_url_code": short_url_code})
                if deleted.deleted_count > 0:
                    return jsonify({"success": True}), 200
                else:
                    return jsonify({"error": "Error occurred while removing the shortened URL."}), 500
            else:
                return jsonify({"error": "Unauthorised"}), 403
        else:
            guest_url_codes = session.get("guest_url_codes", [])
            if short_url_code in guest_url_codes:
                deleted = urls.delete_one({"short_url_code": short_url_code})
                if deleted.deleted_count > 0:
                    guest_url_codes.remove(short_url_code)
                    session["guest_url_codes"] = guest_url_codes
                    session.modified = True
                    return jsonify({"success": True}), 200
                else:
                    return jsonify({"error": "Error occurred while removing the shortened URL."}), 500
    else:
        return jsonify({"error": "Shortened URL not found"}), 404


@main.route("/about")
def about():
    return render_template("about.html")