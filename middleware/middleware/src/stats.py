from spacy.lang.fr.stop_words import STOP_WORDS as stop_words
import re
from src.helpers import PATTERNS

WORD_SPLIT_PATTERN = re.compile(PATTERNS['split_words'])

def basic_filter(stop_words=stop_words, min_len_word=2):
    def wrapped_basic_filter(word):
        if word in stop_words or len(word) < min_len_word:
            return False
        return True
    return wrapped_basic_filter

def word_list_freq(text, filter=basic_filter()):
    """
        For given text, return frequencies of filtered words.

        Parameters
        ----------
        text : str, text on which compute frequencies
        filter : func, default=stat.basic_filter, function that return true or false, use to skip unwanted word

    """
    word_list = WORD_SPLIT_PATTERN.finditer(text.lower())
    word_freq = []
    filtered_sentence = [w.group(0) for w in word_list if filter(w.group(0)) ]
    for w in filtered_sentence:
        word_freq.append(filtered_sentence.count(w))
    return list(zip(filtered_sentence, word_freq))
