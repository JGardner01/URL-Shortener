from flask import render_template, request, redirect, abort
from app import app, urls
from .shortener import generate_short_url_code, validate_custom_short_code, generate_qr_code

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
            "original_url": url,
            "short_url_code": short_url_code
        })

        short_url = request.host_url + short_url_code    #domain + code
        qr = generate_qr_code(short_url)

        return render_template("index.html", short_url=short_url, qr_code_image=qr)

    return render_template("index.html")

@app.route("/<short_url_code>")
def redirect_url(short_url_code):
    url = urls.find_one({"short_url_code" : short_url_code});
    if url:
        return redirect(url["original_url"])
    else:
        return abort(404)   #temporary error message for short url not found