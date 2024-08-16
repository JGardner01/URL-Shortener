from app import urls
import string
import random
import re
import qrcode
from io import BytesIO
import base64

#length set at temporary value 5
def generate_short_url_code(length=5):
    chars = string.ascii_letters + string.digits

    while True:
        short_url = "".join(random.choice(chars) for _ in range(length))
        short_url_exists = urls.find_one({"short_url_code": short_url})
        if not short_url_exists:
            return short_url

def validate_custom_short_code(custom_short_code):
    if not (3 <= len(custom_short_code) <= 20):
        return False, "Custom short code must be between 3 and 20 characters."

    if not re.match("^[a-zA-Z0-9-]+$", custom_short_code):
        return False, "Custom short code must only contain letters, numbers and hyphens(-)."

    if custom_short_code.startswith("-") or custom_short_code.endswith("-"):
        return False, "Custom short code cannot start or end with a hyphen(-)."

    if urls.find_one({"short_url_code": custom_short_code}):
        return False, "Custom short code already exists."

    return True, None


def generate_qr_code(url):
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format("png"))
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
