# your_app/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events

from apscheduler.triggers.interval import IntervalTrigger
from django.utils.timezone import now
import pytz

from .utils.utils import main
from .utils.email_fetcher import check_emails


def job_runner():
    print(f"Running jobs at {now()}")
    main()
    check_emails()


def start():
    scheduler = BackgroundScheduler(timezone=pytz.timezone("Australia/Sydney"))
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # 8 AM, 10 AM, and 2 PM daily
    scheduler.add_job(
        job_runner,
        trigger=CronTrigger(hour='8,10,14', minute='0'),  # 8:00, 10:00, 14:00
        id="daily_jobs",
        replace_existing=True,
    )

    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...")
