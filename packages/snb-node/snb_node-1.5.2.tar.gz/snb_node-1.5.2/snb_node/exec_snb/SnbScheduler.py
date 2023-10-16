from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
import sys

if sys.platform == 'win32':
    jobstores = {'default': SQLAlchemyJobStore(url='sqlite:///snb_node_apscheduler.sqlite')}
else:
    jobstores = { 'default': SQLAlchemyJobStore(url='sqlite:////home/snb_node_apscheduler.sqlite')}

executors = { 'default': {'type': 'threadpool', 'max_workers': 20},    'processpool': ProcessPoolExecutor(max_workers=5)}
job_defaults = { 'coalesce': False,    'max_instances': 3}
scheduler = BackgroundScheduler()
scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

scheduler.start()