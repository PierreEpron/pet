from pathlib import Path
import os, json
import spacy
from spacy.pipeline import EntityRecognizer
from spacy.language import Language
from spacy import displacy
import logging

# CONST From .env
MIDDLEWARE_LOG_PATH = os.environ.get('MIDDLEWARE_LOG_PATH', 'logs/middleware_logs.log')

# Dictionnary with all regex patterns used in models. Geys are names of regex, values are regex to compile
PATTERNS = json.loads(Path(os.path.join(os.path.dirname(__file__), 'regex.json')).read_text(encoding='utf-8'))

# Dictionnary of keyword used for dim. Keys are id of keywords in DIM database, values are words
DIM_KEYWORDS= json.loads(Path(os.path.join(os.path.dirname(__file__), 'dim_keywords.json')).read_text(encoding='utf-8'))

def get_logger():
    '''
        Shorcut for get middleware logger
        
        Returns
        -------
        logger : logging.Logger, logger of middleware.
    '''
    if not Path('logs').is_dir():
        os.mkdir('logs')

    # Get or create logger
    logger = logging.getLogger('middleware')
    logger.setLevel(logging.INFO)
    # Add file handler
    handler = logging.FileHandler(MIDDLEWARE_LOG_PATH, encoding='utf-8')
    logger.addHandler(handler)
    # Set handlers formatter
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(threadName)s :: %(message)s')
    logging.StreamHandler().setFormatter(formatter)
    handler.setFormatter(formatter)
    return logger

def get_custom_ner_path(dirname):
    """
    Helper for get path of a ner model with a given directory.

    Parameters
    ----------
    dirname : str, name of the directory to find ner model.

    Returns
    -------
    data : pathlib.Path, path of ner best model for given dirname.
    """
    return Path(f'../../samples/data/train/{dirname}/output/model-best')

def add_custom_ner(nlp, dirname, name, after='tok2vec'):
    """
    Helper for add a custom ner in a existing spacy pipeline.

    Parameters
    ----------
    nlp : spacy.Language, spacy pipeline where custom ner will be add
    dirname : str, dirname of the directory to find ner model. Used by get_custom_ner_path
    name : str, name of custom ner
    after : str, default="tok2vec", component before custom name
    """
    # Load custom name
    ner = spacy.load(get_custom_ner_path(dirname))
    # Create custom ner factory
    Language.factory(
        name, 
        default_config=ner.get_pipe_config('ner'), 
        func=lambda nlp, name: EntityRecognizer(nlp, name))
    # Rename custom ner pipe
    ner.rename_pipe('ner', name)
    # Add custom ner pipe
    nlp.add_pipe(name, source=ner, after=after)

def extract_ents(doc, labels):
    '''
        Extract entitites in doc.

        Parameters
        ----------
        doc : spacy.Doc, document where to extract entities
        labels : list, list of label (str) of entities to extract

        Returns
        -------
        result : list, entities well formatted.

    '''
    return [{'start':ent.start_char, 'end':ent.end_char, 'label':ent.label_} for ent in doc.ents if ent.label_ in labels]

def get_patterns(pattern_keys):
    '''
        Shorcut to get patterns of regex.json

        Parameters
        ----------
        pattern_keys : str, list of keys of patterns to extract

        Returns
        -------
        result : dict, pattern formatted like key, pattern

    '''
    return {k:v for k, v in PATTERNS.items() if k in pattern_keys}

def extract_sents(doc):
    '''
        Extract sents in doc.

        Parameters
        ----------
        doc : spacy.Doc, document where to extract entities

        Returns
        -------
        feature_name : str, 'sents', the name of feature
        result : list, sents well formatted.

    '''
    return 'sents', [{'start':sent.start_char, 'end':sent.end_char, 'label':str(i)} for i, sent in enumerate(doc.sents) if sent.text.strip() != '']      

def correct_encoding(txt):
    '''
        Correct encoding problems.

        Parameters
        ----------
        txt : str, text to apply encoding correction

        Returns
        -------
        txt : str, text with encoding corrected

    '''    
    return txt.replace('\xa0', ' ').replace('\x92', '\'').replace('\x9c', 'oe') if type(txt) == str else txt

def ner_html(path, docs, manual=False, options={}):
    """
        Shorcut for save docs in html with displacy

        Parameters
        ----------
        path : str or Path, path of data to load
        docs : list, see doc of displacy.
        manual : bool, see doc of displacy.
        options : dict, see doc of displacy.
    """
    path = Path(path) if isinstance(path, str) else path
    path.write_text(displacy.render(docs, style='ent', manual=manual, options=options, page=True), encoding='utf-8')

def read_jsonl(path, encoding='utf-8'):
    """
        Shortcut for read jsonl file

        Parameters
        ----------
        path : str or Path, path of data to read
        encoding : str, default='utf-8', encoding format to read.
    """
    path = Path(path) if isinstance(path, str) else path
    return [json.loads(line) for line in path.read_text(encoding=encoding).strip().split('\n')]

def write_jsonl(path, data, encoding='utf-8'):
    """
        Shortcut for write jsonl file

        Parameters
        ----------
        path : str or Path, path of data to read
        encoding : str, default='utf-8', encoding format to write.
    """
    path = Path(path) if isinstance(path, str) else path
    path.write_text('\n'.join([json.dumps(item) for item in data]), encoding=encoding)