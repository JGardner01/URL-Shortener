from app import db
import string
import random
import qrcode
from io import BytesIO
import base64

#length set at temporary value 5
def generate_short_url_code(length=5):
    chars = string.ascii_letters + string.digits

    while True:
        short_url = "".join(random.choice(chars) for _ in range(length))
        short_url_exists = db.urls.find_one({"short_url_code": short_url})
        if not short_url_exists:
            return short_url

#def validate_custom_short_code:
#to implement

def generate_qr_code(url):
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format("png"))
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
