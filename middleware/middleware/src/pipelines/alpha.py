from pathlib import Path
import spacy
from .pipeline_ctrl import PipelineCtrl
from src.components import section_splitter
from src.helpers import extract_sents

class Alpha(PipelineCtrl):
    def __init__(self) -> None:
        super().__init__(version="0.1", force_update=False)
        self.sections_patterns = ['intro', 'ctx', 'tech', 'obs', 'ccl']
        self.load_model()

    def __call__(self, text, features) -> None:
        doc = self.nlp(text)
        self.add_feature(features, section_splitter.extract_sections(doc))
        self.add_feature(features, extract_sents(doc))

    def load_model(self) -> None:
        self.nlp = spacy.load("fr_dep_news_trf")
        self.nlp.add_pipe("sections_splitter", config={"patterns": self.sections_patterns})

    def save_model(self, path) -> None:
        path = Path(path) if isinstance(path, str) else path
        self.nlp.to_disk(path / self.get_fullname())