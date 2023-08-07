import requests
import secrets_handler

from . import AttributedDataItem


def fetch_pronunciation(word: str, language = "no") -> AttributedDataItem:
    api_key = secrets_handler.secrets["FORVO_API_KEY"]
    url = "https://apifree.forvo.com/key/{api_key}/format/json/action/word-pronunciations/word/{word}/language/{language}"

    response = requests.get(url.format(api_key=api_key, word=word, language=language))
    response.raise_for_status()

    try:
        mp3_url = response.json()["items"][0]["pathmp3"]
        attribution = f"Pronunciation by Forvo.com user {response.json()['items'][0]['username']}."
    except IndexError:
        return None

    return AttributedDataItem(_fetch_pronunciation_data(mp3_url), attribution)


def _fetch_pronunciation_data(url: str) -> bytes:
    response = requests.get(url)
    response.raise_for_status()
    return response.content


