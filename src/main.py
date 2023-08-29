import image_fetcher
import pronunciation_fetcher
import translation_fetcher
import words_fetcher
import generator
from dictionary_api_client import DictionaryAPIClient
from models import NorwegianWord
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("log.txt", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


if __name__ == "__main__":
    words = []
    dictionary_api_client = DictionaryAPIClient()
    for i, word in enumerate(words_fetcher.fetch_words()):
        entry = dictionary_api_client.lookup(word)
        article = ""

        if entry is None:
            logging.warning(f"Could not find {word} in dictionary.")
        else:
            article = "/".join(sorted(map(lambda g: g.article, entry.genders), reverse=True))
        
        pronunciation = pronunciation_fetcher.fetch_pronunciation(word)
        if pronunciation is None:
            logging.warning(f"Could not find pronunciation for {word}.")
        else:
            pronunciation.save(f"data/{word}.mp3")

        translation = translation_fetcher.fetch_translation(word)

        image = image_fetcher.fetch_image(translation)
        if image is None:
            logging.warning(f"Could not find image for {word}/{translation}.")
        else:
            image.save(f"data/{word}.jpg")

        words.append(NorwegianWord(word, pronunciation, article, image, translation, i))
        logging.info(f"Added {word} to deck: {words[-1]}")
    
    deck = generator.generate_anki_package(words)
    deck.write_to_file("data/Norwegian 1000 Most Common Words - Pronunciation, Image, English Translation, and Article.apkg")
    logging.info("Complete!")


