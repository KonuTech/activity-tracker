import datetime
from collections import defaultdict
from flask import Blueprint, render_template, request, redirect, url_for


pages = Blueprint("activities", __name__, template_folder="templates", static_folder="static")
activities = ["Test activity"]
completions = defaultdict(list)


def date_range(start: datetime.date):
    dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
    return dates


@pages.context_processor
def add_calc_date_range():
    def date_range(start: datetime.date):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates

    return {"date_range": date_range}


@pages.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
    else:
        selected_date = datetime.date.today()
    return render_template(
        "index.html",
        activities=activities,
        selected_date=selected_date,
        completions=completions[selected_date],
        title="Activity Tracker - Home"
    )


@pages.route("/add", methods=["GET", "POST"])
def add_activity():
    if request.method == "POST":
        activity = request.form.get("activity")
        activities.append(activity)
    return render_template(
        "add_activity.html",
        title="Activity Tracker - Add Activity",
        selected_date=datetime.date.today()
    )


@pages.route("/complete", methods=["POST"])
def complete():
    date_string = request.form.get("date")
    activity = request.form.get("activityName")
    date = datetime.date.fromisoformat(date_string)
    completions[date].append(activity)

    return redirect(url_for("activities.index", date=date_string))
