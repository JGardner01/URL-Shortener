from flask import render_template, request
from app import app


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return "Shortened URL Placeholder"
    return render_template("index.html")

