from pathlib import Path
import json

PATTERNS = json.loads(Path('src/regex.json').read_text(encoding='utf-8'))

def get_patterns(pattern_keys):
    return [(k, v) for k, v in PATTERNS.items() if k in pattern_keys]

def extract_sents(doc):
    return 'sents', [{'start':sent.start_char, 'end':sent.end_char, 'label':str(i)} for i, sent in enumerate(doc.sents) if sent.text.strip() != '']      

def correct_encoding(txt):
    return txt.replace('\xa0', ' ').replace('\x92', '\'').replace('\x9c', 'oe') if type(txt) == str else txt