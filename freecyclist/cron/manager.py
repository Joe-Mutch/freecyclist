import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from freecycle import FreecycleScraper
from freecyclist.models import User
from freecyclist import app

def parse_alerts():
    with app.app_context():
        users = User.query.all()
        for user in users:
            alerts = user.get_alerts()
            for alert in alerts:
                checker = FreecycleScraper(alert=alert, locations=alert.get_location_names(), keywords=alert.get_keyword_names())
                checker.find()

# parse_alerts()

import logging

log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=parse_alerts,
    trigger=IntervalTrigger(seconds=10),
    id='printing_job',
    name='Print date and time every five seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

