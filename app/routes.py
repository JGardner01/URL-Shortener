from flask import render_template, request
from app import app
from .shortener import generate_short_url_code


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        short_url_code = generate_short_url_code()
        #save url and short url code to database
        return request.host_url + short_url_code
    return render_template("index.html")

