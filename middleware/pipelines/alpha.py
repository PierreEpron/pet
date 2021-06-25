from re import I
import spacy
from .pipeline_ctrl import PipelineCtrl
from ..components.section_splitter import extract_sections

class Alpha(PipelineCtrl):
    def __init__(self, version) -> None:
        super().__init__(version)
        self.sections_patterns = [
            ('intro', r'[\s\n\r]*contexte dans lequel l[’\']*(?:examen|étude) est réalisée? ?:?[\s\n\r]*'),
            ('ctx', r'[\s\n\r]*technique de l\'examen ?:?[\s\n\r]*'),
            ('tech', r'[\s\n\r]*[a-zA-Z0-9,/\'\-éà ]*(, on observe :|apporte les informations suivantes ?:?| (mettent|on met) en évidence :)[\s\n\r]*'),
            ('obs', r'[\s\n\r]*(en )*conclusion ?:?[\s\n\r]*'),
            ('ccl', r'[\s\n\r]*$')]
        self.load_model()

    def __call__(self, text, features) -> None:
        doc = self.nlp(text)
        self.add_feature(features, extract_sections(doc))

    def load_model(self) -> None:
        self.nlp = spacy.load("fr_dep_news_trf")
        self.nlp.add_pipe("sections_split", config={"patterns": self.sections_patterns})

