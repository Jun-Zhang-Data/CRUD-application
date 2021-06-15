import os

from flask import Flask
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy
from flask import redirect

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "dailyactivitiesdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


class Activity(db.Model):
    activity_name = db.Column(db.String(90), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)
    
    

@app.route('/', methods=["GET", "POST"])
def home():
    activities = None
    if request.form:
        try:
            activity = Activity(activity_name=request.form.get("activity_name"))
            db.session.add(activity)
            db.session.commit()
        except Exception as e:
            print("Failed to add activity")
            print(e)
    activities = Activity.query.all()
    return render_template("home.html", activities=activities)

@app.route("/update", methods=["POST"])
def update():
    try:
        new_activity_name = request.form.get("newactivity")
        old_activity_name = request.form.get("oldactivity")
        activity = Activity.query.filter_by(activity_name=old_activity_name).first()
        activity.activity_name = new_activity_name
        db.session.commit()
    except Exception as e:
        print("Couldn't update activity")
        print(e)
    return redirect("/")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
