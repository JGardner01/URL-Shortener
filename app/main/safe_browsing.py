from flask import current_app
import requests

def check_url_safety(url):
    api_key = current_app.config["GOOGLE_API_KEY"]
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    payload = {
        "client": {
            "clientId":         "urlshortener",
            "clientVersion":    "1.0.0"
        },
        "threatInfo": {
            "threatTypes":      ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes":    ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries":    [
                {
                    "url": url
                }
            ]
        }
    }

    response = requests.post(endpoint, json=payload)
    if response.status_code == 200:
        result = response.json()
        if "matches" in result:
            return False, "The URL entered was found to be potentially malicious."
        else:
            return True, None
    else:
        return False, "Error occurred checking the URL safety."
