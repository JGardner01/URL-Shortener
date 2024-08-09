from flask import render_template, request, redirect, abort
from app import app, urls
from .shortener import generate_short_url_code


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")

        if not (url.startswith("http://") or url.startswith(("https://"))):
            url = "http://" + url

        short_url_code = generate_short_url_code()

        urls.insert_one({
            "original_url": url,
            "short_url_code": short_url_code
        })

        return request.host_url + short_url_code
    return render_template("index.html")

@app.route("/<short_url_code>")
def redirect_url(short_url_code):
    url = urls.find_one({"short_url_code" : short_url_code});
    if url:
        return redirect(url["original_url"])
    else:
        return abort(404)   #temporary error message for short url not found