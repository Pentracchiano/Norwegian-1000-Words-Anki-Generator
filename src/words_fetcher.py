import requests


def _download_words(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def _parse_words(words: str, limit: int = 1000) -> list[str]:
    return [line.split(' ')[0] for line in words.split('\n')[:limit]]


def fetch_words(limit: int = 1000) -> list[str]:
    # Props to https://github.com/hermitdave/FrequencyWords for the word list
    # and to
    # P. Lison and J. Tiedemann, 2016, OpenSubtitles2016: Extracting Large Parallel Corpora from Movie and TV Subtitles. In Proceedings of the 10th International Conference on Language Resources and Evaluation (LREC 2016)
    # for the word data. 
    # TODO add this attributions to the readme too
    # check first if data/words.txt exists
    try:
        with open('data/words.txt', 'r', encoding='utf-8') as f:
            return f.read().split('\n')[:limit]
    except FileNotFoundError:
        print("Downloading words.txt...")

    url = 'https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/no/no_50k.txt'
    words = _download_words(url)
    return _parse_words(words, limit)

if __name__ == '__main__':
    # write all words to a file in data/
    with open('data/words.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fetch_words()))