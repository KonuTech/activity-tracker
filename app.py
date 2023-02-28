from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="Activity Tracker - Home")


@app.route("/add", methods=["GET", "POST"])
def add_activity():
    return render_template("add_habit.html", title="Activity Tracker - Add Activity")
