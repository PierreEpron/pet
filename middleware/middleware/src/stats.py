from spacy.lang.fr.stop_words import STOP_WORDS as stop_words
import re
from src.helpers import PATTERNS

WORD_SPLIT_PATTERN = re.compile(PATTERNS['split_words'])

def word_list_freq(text, stop_words=stop_words):
    """
        For given text, return frequencies of words without given stopwords.

        Parameters
        ----------
        text : str, text on which compute frequencies
        stop_words : list,default=spacy.lang.fr.stop_words.STOP_WORDS, words skipped when computing frequencies.

    """
    word_list = WORD_SPLIT_PATTERN.finditer(text.lower())
    word_freq = []
    filtered_sentence = [w.group(0) for w in word_list if not w.group(0) in stop_words]
    for w in filtered_sentence:
        word_freq.append(filtered_sentence.count(w))
    return list(zip(filtered_sentence, word_freq))
