import os

import requests
import json
import time
from urllib.request import urlretrieve


url = "https://api.soundoftext.com/sounds"


def _get_number_url(number, language_id):
    body = json.dumps({
        "engine": "Google",
        "data": {
            "text": str(number),
            "voice": language_id
        }
    })
    response = requests.post(
        url=url,
        headers={'content-type': 'application/json'},
        data=body
    )
    if response.status_code != 200:
        raise ConnectionError("Cannot load text for {} in language {}:\n{}".format(number, language_id, response.text))
    sound_id = json.loads(response.text)["id"]

    while True:
        location_response = json.loads(requests.get(url="/".join([url, sound_id])).text)
        if ("success" in location_response.keys() and location_response["success"] is False) or location_response["status"] == "Error":
            raise ConnectionError("Error occured while loading path:\n" + str(location_response))
        if location_response["status"] == "Done":
            return location_response["location"]
        time.sleep(0.1)


def download_sound(number, language_id, location):
    file_path = os.path.join(location, "{}.mp3".format(number))

    if not os.path.isfile(file_path):
        urlretrieve(_get_number_url(number, language_id), file_path)

    return file_path
