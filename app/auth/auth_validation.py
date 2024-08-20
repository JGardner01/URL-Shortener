from flask import current_app
import re

def validate_new_username(username):
    users = current_app.users
    username_exists = users.find_one({"username": username})
    if username_exists:
        return False, "User already exists."

    #username must be between 3 and 15 characters
    if not (3 <= len(username) <= 15):
        return False, "Username must be 3-15 characters long."
    #username must start with a letter
    if not username[0].isalpha():
        return False, "Username must start with a letter."
    #user name must contain only letters and numbers
    if not re.match("^[a-zA-Z0-9]$", username):
        return False, "Username may only contain letters and numbers."

    return True, None


def validate_new_password(password, confirm_password):
    #password must be at least 8 characters
    if len(password) < 7:
        return False, "Password must be at least 8 characters long."
    #password must include at least 1 upper case character
    if not re.search("[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    #password must include at least 1 lower case character
    if not re.search("[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    #password must include at least 1 number character
    if not re.search("[0-9]", password):
        return False, "Password must contain at least one numeric character."
    #password must include at least 1 special character
    if not re.search(r"[!#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~]", password):
        return False, "Password must contain at least one special character."
    #password must not contain spaces
    if " " in password:
        return False, "Password must not contain spaces."
    #password and confirm password must match
    if password != confirm_password:
        return False, "Passwords do not match."

    return True, None