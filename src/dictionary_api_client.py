import requests


class DictionaryAPIClient:
    """
    A client for the dictionary API ordbokene.no. Swagger: https://ordbokene.no/api/swagger-ui.html
    It only supports Bokmål, but it can be extended to support Nynorsk as the API supports it.
    """
    def __init__(self, session: requests.Session = None):
        self._word_finding_url = 'https://ord.uib.no/api/articles?w={}&dict=bm&scope=ei'
        self._article_lookup_url = 'https://ord.uib.no/bm/article/{}.json'

        self._session = requests.Session() if session is None else session
        self._session.headers.update({'User-Agent': 'Norwegian-Anki/1.0 (https://github.com/Pentracchiano/Norwegian-1000-Words-Anki-Generator)'})
        self._session.headers.update({'Accept': 'application/json'})
        self._session.headers.update({'Accept-Encoding': 'gzip, deflate, br'})

    def find_ids_by_word(self, word: str) -> list[int]:
        response = self._session.get(self._word_finding_url.format(word))
        response.raise_for_status()
        return response.json()["articles"]["bm"]
    
    def article_by_id(self, id: int) -> dict:
        response = self._session.get(self._article_lookup_url.format(id))
        response.raise_for_status()
        return response.json()
    
    def article_by_word(self, word: str) -> dict:
        ids = self.find_ids_by_word(word)
        if len(ids) == 0:
            return None
        return self.article_by_id(ids[0])

