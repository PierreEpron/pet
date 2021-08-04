from spacy.language import Language
from spacy.tokens import Doc
import re, json
from src.helpers import get_patterns

@Language.factory("regex_matcher", default_config={"patterns": []})
def create_regex_matcher_component(nlp: Language, name: str, patterns: list):
    return RegexMatcherComponent(nlp, patterns)

class RegexMatcherComponent:
    def __init__(self, nlp: Language, patterns: list):
        self.patterns = self.load_patterns(get_patterns(patterns))
        if not Doc.has_extension("regex_matchs"):
            Doc.set_extension("regex_matchs", default=[])

    def __call__(self, doc: Doc) -> Doc:
        
        return doc

    def to_disk(self, path, exclude=tuple()):
        data_path = path / "patterns.json"
        
        if not path.is_dir():
            path.mkdir()

        data_path.write_text(json.dumps({k:v for k, v in get_patterns(list(self.patterns.keys())).items()}), encoding="utf-8")

    def from_disk(self, path, exclude=tuple()):        
        data_path = path / "patterns.json"

        self.patterns = json.loads(data_path.read_text())

    def load_patterns(self, patterns):
        return {k:re.compile(v, re.I) for k, v in patterns.items()}

def extract_matchs(doc):
    pass
    # return 'sections', [{'start':section.start_char, 'end':section.end_char, 'label':section.label_} for section in doc._.sections]      

