from spacy.lang.fr.stop_words import STOP_WORDS as stop_words
import re
from src.helpers import PATTERNS

WORD_SPLIT_PATTERN = re.compile(PATTERNS['split_words'])

STOP_WORDS = set(list(stop_words)+['xxxx','XXXX'])

def basic_filter(stop_words=STOP_WORDS, min_len_word=2):
    '''
        Wrapper to filter text with stop words and min size of word
        
        Parameters
        ----------
        stop_words : set, default=stats.STOP_WORDS stop words in str to exclude
        min_len_word : int, default=2, minimum size of word to keep

        Returns
        -------
        wrapped_basic_filter : func, function taking word and return if true or false based on filter.

    '''
    def wrapped_basic_filter(word):
        if word in stop_words or len(word) < min_len_word:
            return False
        return True
    return wrapped_basic_filter

def word_list_freq(text, filter=basic_filter()):
    '''
        For given text, return frequencies of filtered words.

        Parameters
        ----------
        text : str, text on which compute frequencies
        filter : func, default=stats.basic_filter, function that return true or false, use to skip unwanted word
        Returns
        -------
        word_freq : list, a list of dict with value as str of word and count as freq of word.

    '''
    # Split text into word
    word_list = WORD_SPLIT_PATTERN.finditer(text.lower())
    word_freq = []
    # Filter words
    filtered_words= [w.group(0) for w in word_list if filter(w.group(0))]
    # Create unique set of words
    unique_words= set(filtered_words)
    # Count freq of words
    for w in unique_words:
        word_freq.append(filtered_words.count(w))
    # Returning formatted words frequencies 
    return [{"value":word,"count":freq} for word, freq in zip(unique_words, word_freq)]

def gather_identity(text, features):
    '''
        Postprocess identity (age, gender) extraction in features of a document
        
        Parameters
        ----------
        text : str, text of the document
        features : dict, features of the document

        Returns
        -------
        result : dict, contain gender and age features postprocess.

    '''
    # Retrieve identities features
    identity = list(filter(lambda feature: feature['name'] == 'identity', features))
    result = {}
    # if there is identities features
    if len(identity) != 0:
        for item in identity[0]['sources'][0]['items']:
            # if it's age feature
            if item['label'] == 'age':
                # Postprocess
                txt = text[item['start']:item['end']]
                result.update({item['label']:txt.split('(')[1].split(' ')[0].lower()})
            # if it's gender feature
            elif item['label'] == 'gender':
                # Postprocess
                txt = text[item['start']:item['end']]
                result.update({item['label']:txt.split(' ')[0].lower()})
    # Return features postprocessed
    return result
