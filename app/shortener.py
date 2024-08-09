import string
import random

#length set at temporary value 5
def generate_short_url_code(length=5):
    chars = string.ascii_letters + string.digits

    while True:
        short_url = "".join(random.choice(chars) for _ in range(length))
        #check if the url exists in database
        #genrate again if it does already exist
        return short_url