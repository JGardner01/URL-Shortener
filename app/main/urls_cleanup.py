from flask import current_app
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone

def remove_expired_urls(app):
    with app.app_context():
        urls = current_app.urls

        current_time = datetime.now(timezone.utc)
        urls.delete_many({
            "$or": [
                {"expiration_date": {"$lt": current_time}},
                {"$and": [
                    {"click_limit": {"$exists": True}},
                    {"$expr": {"$gte": ["$click_count", "$click_limit"]}}
                ]}
            ]
        })


def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=remove_expired_urls, trigger="interval", hours=1, args=[app])
    scheduler.start()