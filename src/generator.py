import genanki
from pathlib import Path
from dataclasses import dataclass


class NorwegianNote(genanki.Note):
    """
    The GUID for the note is generated from the Norwegian word only, as it's the unique identifier for the note.
    This can make re-generation of the deck easier, as the GUIDs will remain the same for the notes that are unchanged.
    This will prevent Anki from creating duplicate notes when importing the deck.

    The notes are sorted by the frequency of the word, so that the most common words are shown first.
    """
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])
    
    @property
    def sort_field(self):
        # Frequency order
        return self.fields[-1]

def _extract_file_name(path):
    return Path(path).name

def _to_sound_field(path):
    file_name = _extract_file_name(path)
    return f'[sound:{file_name}]'

def _to_image_field(path):
    file_name = _extract_file_name(path)
    return f'<img src="{file_name}">'


def _generate_anki_deck(norwegian_words):
    # Randomly generated IDs and then hardcoded to keep them consistent
    deck_id = 74381608  
    model_id = 39838499

    card_model = genanki.Model(
        model_id=model_id,
        name='Norwegian 1000 Most Common Words - Pronunciation, Image, English Translation, and Article',
        fields=[
            {'name': 'norwegian_word'},
            {'name': 'pronunciation'},
            {'name': 'article'},
            {'name': 'image'},
            {'name': 'english_translation'},
            {'name': 'frequency_order'}
        ],
        templates=[
            {
                'name': 'Norsk to Engelsk',
                'qfmt': '{{article}} {{norwegian_word}}<br>{{pronunciation}} {{image}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{english_translation}}'
            },
            {
                'name': 'English to Norwegian',
                'qfmt': '{{english_translation}} <br> {{image}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{article}} {{norwegian_word}}<br>{{pronunciation}}'
            }
        ]
    )

    deck = genanki.Deck(deck_id, 'Norwegian 1000 Most Common Words - Pronunciation, Image, English Translation, and Article')

    for word in norwegian_words:
        note = NorwegianNote(
            model=card_model,
            fields=[
                word['norwegian'],
                _to_sound_field(word['pronunciation']),
                word['article'],
                _to_image_field(word['image']),
                word['english'],
                word['frequency']
            ]
       )
        deck.add_note(note)

    return deck


@dataclass
class NorwegianWord:
    norwegian: str
    pronunciation: str
    article: str
    image: str
    english: str
    frequency: str


def generate_anki_package(norwegian_words: list[NorwegianWord]) -> genanki.Package:
    """
    Generates an Anki deck package from the given list of Norwegian words.
    You can then write the package to a file using the `write_to_file` method, using the `.apkg` file extension.
    :example: 
    norwegian_words = [
        NorwegianWord(
            norwegian='hund',
            pronunciation='long/path/hund.mp3',
            article='en',
            image='long/path/hund.jpg',
            english='dog',
            frequency='123'
        )
    ]

    """
    deck = _generate_anki_deck(norwegian_words)
    package = genanki.Package(deck)
    package.media_files = [word.image for word in norwegian_words]
    return package
