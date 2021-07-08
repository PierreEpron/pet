from pathlib import Path
import json
from spacy import displacy

PATTERNS = json.loads(Path('src/regex.json').read_text(encoding='utf-8'))

def get_patterns(pattern_keys):
    return {k:v for k, v in PATTERNS.items() if k in pattern_keys}

def extract_sents(doc):
    return 'sents', [{'start':sent.start_char, 'end':sent.end_char, 'label':str(i)} for i, sent in enumerate(doc.sents) if sent.text.strip() != '']      

def correct_encoding(txt):
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
    path = Path(path) if isinstance(path, str) else path
    return [json.loads(line) for line in path.read_text(encoding=encoding).strip().split('\n')]