import time
from typing import Literal
import requests
import secrets_handler


class Image:
    def __init__(self, data: bytes, attribution = None):
        self.data = data
        self.attribution = attribution if attribution is not None else "Photo by Pixabay.com"

    def save(self, path: str):
        with open(path, "wb") as f:
            f.write(self.data)


def fetch_image(word: str, language: str = None, image_type: Literal["photo", "illustration", "vector"] = None, retry_on_throttle=True) -> Image:
    secret = secrets_handler.secrets["PIXABAY_API_KEY"]
    url = f"https://pixabay.com/api/"
    response = requests.get(url, params={
        "key": secret,
        "q": word,
        "lang": language,
        "image_type": image_type,
        "per_page": 3,  # minimum
        "safesearch": True,
        "editors_choice": True
    })
    if response.status_code == 429 and retry_on_throttle:
        return _handle_throttle(response, fetch_image, word, language, image_type, retry_on_throttle=False)

    response.raise_for_status()
    content = response.json()
    image_url = content["hits"][0]["webformatURL"]
    return Image(_fetch_image_data(image_url, retry_on_throttle))


def _fetch_image_data(image_url, retry_on_throttle=True):
    response = requests.get(image_url)
    if response.status_code == 429 and retry_on_throttle:
        return _handle_throttle(response, _fetch_image_data, image_url, retry_on_throttle=False)

    response.raise_for_status()
    return response.content


def _handle_throttle(response, func, *args, **kwargs):
    print("Throttled. Retrying...")
    # headers are X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
    # so let's use the Reset in this case
    # https://pixabay.com/api/docs/#api_rate_limit
    delay = int(response.headers["X-RateLimit-Reset"])
    time.sleep(delay + 1)

    return func(*args, **kwargs)
    

if __name__ == "__main__":
    thing = "egg"
    image = fetch_image(thing)
    image.save(f"{thing}.jpg")
    
