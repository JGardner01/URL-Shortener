from flask import session, current_app
from flask_login import current_user

def transfer_guest_urls():
    guest_url_codes = session.get("guest_url_codes", [])
    if guest_url_codes:
        urls = current_app.urls
        user_id = current_user.get_id()

        urls.update_many(
            {"short_url_code": {"$in": guest_url_codes}},
            {"$set": {"user_id": user_id}}
        )

        session.pop("guest_url_codes", None)     #testing