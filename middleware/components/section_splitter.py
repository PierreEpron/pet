from spacy.language import Language
from spacy.tokens import Doc
import re

@Language.factory("sections_splitter", default_config={"patterns": []})
def create_sections_splitter_component(nlp: Language, name: str, patterns: list):
    return SectionSplitterComponent(nlp, patterns)

class SectionSplitterComponent:
    def __init__(self, nlp: Language, patterns: list):
        self.patterns = {p[0]:re.compile(p[1], re.I) for p in patterns}
        if not Doc.has_extension("sections"):
            Doc.set_extension("sections", default=[])

    def __call__(self, doc: Doc) -> Doc:
        start, end = 0, 0
        sections = []
        for k, v in self.patterns.items():
            match = v.search(doc.text)
            if match == None:
                return doc
            end = match.span()[0]
            span = doc.char_span(start, end, label=k)
            if span == None:
                return doc
            sections.append(span)
            start = match.span()[1]
        doc._.sections = sections
        return doc

def extract_sections(doc):
    return 'sections', [{'start':section.start, 'end':section.end, 'label':section.label} for section in doc._.sections]      

