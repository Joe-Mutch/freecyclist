import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from freecycle import AlertChecker
from freecyclist.models import User

def parse_alerts():
    users = User.query.all()
    for user in users:
        alerts = user.get_alerts()
        for alert in alerts:
            checker = AlertChecker(alert)
            checker.find()

# parse_alerts()

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=parse_alerts,
    trigger=IntervalTrigger(seconds=60),
    id='printing_job',
    name='Print date and time every five seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

