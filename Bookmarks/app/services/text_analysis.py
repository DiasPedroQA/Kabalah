# pylint: disable=C

def analyze_text(text):
    """
    Analisa um texto fornecido.
    :param text: str
    :return: dict
    """
    words = text.split()
    char_count = len(text)
    word_count = len(words)

    return {
        "original_text": text,
        "char_count": char_count,
        "word_count": word_count,
        "words": words
    }
