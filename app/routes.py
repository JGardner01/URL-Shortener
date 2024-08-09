from flask import render_template, request
from app import app, urls
from .shortener import generate_short_url_code


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        short_url_code = generate_short_url_code()

        urls.insert_one({
            "url": url,
            "short_url_code": short_url_code
        })

        return request.host_url + short_url_code
    return render_template("index.html")

