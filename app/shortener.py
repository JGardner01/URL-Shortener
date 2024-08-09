from app import db

import string
import random


#length set at temporary value 5
def generate_short_url_code(length=5):
    chars = string.ascii_letters + string.digits

    while True:
        short_url = "".join(random.choice(chars) for _ in range(length))
        short_url_exists = db.urls.find_one({"short_url_code": short_url})
        if not short_url_exists:
            return short_url
