from pathlib import Path
import spacy
from thinc.api import Config
from .pipeline_ctrl import PipelineCtrl
from src.components import section_splitter
from src.components import regex_matcher
from src.helpers import extract_sents

class Alpha(PipelineCtrl):
    def __init__(self) -> None:
        super().__init__(version="0.1", force_update=False)
        self.sections_patterns = ['intro', 'ctx', 'tech', 'obs', 'ccl']
        self.regex_patterns = {'identity':['gender', 'age'], 'medical':['suvmax', 'medobj_size']}
        self.build_model()

    def __call__(self, text, features) -> None:
        doc = self.nlp(text)
        self.add_feature(features, section_splitter.extract_sections(doc))
        self.add_feature(features, extract_sents(doc))
        for feature in regex_matcher.extract_matchs(doc):
            self.add_feature(features, feature)
            
    def build_model(self) -> None:
        self.nlp = spacy.load("fr_dep_news_trf")
        self.nlp.add_pipe("sections_splitter", config={"patterns": self.sections_patterns})
        self.nlp.add_pipe("regex_matcher", config={"patterns": self.regex_patterns}),

    def load_model(self, path) -> None:
        path = Path(path) if isinstance(path, str) else path
        config = Config().from_disk(path / self.get_fullname() / "config.cfg")
        lang_cls = spacy.util.get_lang_class(config["nlp"]["lang"])
        self.nlp = lang_cls.from_config(config)
        self.nlp.from_disk(path / self.get_fullname())

    def save_model(self, path) -> None:
        path = Path(path) if isinstance(path, str) else path
        self.nlp.to_disk(path / self.get_fullname())