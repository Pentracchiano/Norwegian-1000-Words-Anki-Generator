import image_fetcher
import pronunciation_fetcher
import words_fetcher
import generator
import dictionary_api_client
from . import NorwegianWord


if __name__ == "__main__":
    words = []
    for i, word in enumerate(words_fetcher.fetch_words()):
        entry = dictionary_api_client.lookup(word)
        article = ""

        if entry is None:
            print(f"Could not find {word} in dictionary.")
        else:
            article = "/".join(sorted(map(lambda g: g.article, entry.genders)), reverse=True)
        
        image = image_fetcher.fetch_image(word)
        if image is None:
            print(f"Could not find image for {word}.")
        else:
            image.save(f"data/{word}.jpg")

        pronunciation = pronunciation_fetcher.fetch_pronunciation(word)
        if pronunciation is None:
            print(f"Could not find pronunciation for {word}.")
        else:
            pronunciation.save(f"data/{word}.mp3")

        translation = translation_fetcher.fetch_translation(word)

        words.append(NorwegianWord(word, pronunciation, article, image, translation, i))
        print(f"Added {word} to deck: {words[-1]}")
    
    deck = generator.generate_anki_package(words)
    deck.write_to_file("data/Norwegian 1000 Most Common Words - Pronunciation, Image, English Translation, and Article.apkg")


