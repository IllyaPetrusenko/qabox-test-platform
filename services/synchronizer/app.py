from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from flask_pymongo import PyMongo
from budgets import ListOfBudgets
from config import host, offset

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://82.144.223.29:27021/budgets"
mongo = PyMongo(app)


def add_budgets_to_db():
    records = ListOfBudgets(host=host, offset=offset)
    records.write_releases_into_db()
    return records


pp_scheduler = BackgroundScheduler()  # Scheduler object
pp_scheduler.add_job(add_budgets_to_db, 'interval', seconds=20)  # Interval 3 minutes
pp_scheduler.start()


@app.route("/")
def home_page():
    return 'Synchronizer is ready to use'


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5001)
