import datetime
import uuid
from flask import Blueprint, current_app, render_template, request, redirect, url_for


pages = Blueprint("activities", __name__, template_folder="templates", static_folder="static")
# activities = ["Test activity"]
# completions = defaultdict(list)


# def date_range(start: datetime.datetime):
#     dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
#     return dates


@pages.context_processor
def add_calc_date_range():
    def date_range(start: datetime.datetime):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates

    return {"date_range": date_range}


def today_at_midnight():
    today = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day)  # by default, time, min, sec are 0


@pages.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    else:
        selected_date = today_at_midnight()

    activities_on_date = current_app.db.activity.find({"added": {"$lte": selected_date}})

    completions = [
        activity["activity"] for activity in current_app.db.completions.find({"date": selected_date})
    ]

    return render_template(
        "index.html",
        activities=activities_on_date,
        selected_date=selected_date,
        completions=completions,
        title="Activity Tracker - Home"
    )


@pages.route("/complete", methods=["POST"])
def complete():
    date_string = request.form.get("date")
    date = datetime.datetime.fromisoformat(str(date_string))
    activity = request.form.get("activityId")

    # completions[date].append(activity)
    current_app.db.completions.insert_one({"date": date, "activity": activity})

    return redirect(url_for("activities.index", date=date_string))


@pages.route("/add", methods=["GET", "POST"])
def add_activity():
    today = today_at_midnight()

    if request.form:
        current_app.db.activity.insert_one(
            {"_id": uuid.uuid4().hex, "added": today, "name": request.form.get("activity")}
        )

    # if request.method == "POST":
    #     activity = request.form.get("activity")
    #     activities.append(activity)
    return render_template(
        "add_activity.html",
        title="Activity Tracker - Add Activity",
        selected_date=today
    )
