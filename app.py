from flask import Flask, render_template, request

app = Flask(__name__)

activities = ["Test activity", "Test activity 2"]


@app.route("/")
def index():
    return render_template("index.html", activities=activities, title="Activity Tracker - Home")


@app.route("/add", methods=["GET", "POST"])
def add_activity():
    if request.method == "POST":
        activity = request.form.get("activity")
        activities.append(activity)
    return render_template("add_activity.html", title="Activity Tracker - Add Activity")
