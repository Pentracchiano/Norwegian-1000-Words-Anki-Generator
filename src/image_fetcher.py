from typing import Literal
import requests
import secrets_handler


class Image:
    def __init__(self, data: bytes):
        self.data = data

    def save(self, path: str):
        with open(path, "wb") as f:
            f.write(self.data)


def fetch_image(word: str, language: str = None, image_type: Literal["photo", "illustration", "vector"] = None) -> Image:
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
    response.raise_for_status()
    content = response.json()
    image_url = content["hits"][0]["webformatURL"]
    return Image(_fetch_image_data(image_url))


def _fetch_image_data(image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    return response.content


if __name__ == "__main__":
    thing = "egg"
    image = fetch_image(thing)
    image.save(f"{thing}.jpg")
    
