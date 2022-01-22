from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import web_scraping_practice

app = Flask(__name__)
app.secret_key = "key"
app.permanent_session_lifetime = timedelta(minutes = 5)

@app.route("/")
def home():
    return render_template("index.html",PageTitle = "Home")

@app.route("/jobs", methods = ["POST", "GET"])
def jobs():
    if request.method == "POST":
        job = request.form.get("job")
        web_scraping_practice.jobscrape(job)
        job = ''
    return render_template("jobsDisplay.html")


if __name__ == "__main__":
    # db.create_all()
    app.run(debug = True)