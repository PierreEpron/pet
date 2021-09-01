from pathlib import Path
from numpy import select
import spacy
from thinc.api import Config
from src.pipelines.pipeline_ctrl import PipelineCtrl
from src.components import section_splitter
from src.components import regex_matcher
from src.components import pysbd_sentence_boundaries
from src.helpers import extract_sents, add_custom_ner, extract_ents

SUV_NER_PATH = 'suv_28_09_21'
TREATMENT_NER_PATH = 'treatment_28_09_21'

class Alpha(PipelineCtrl):
    name = "Alpha"
    version="0.1"
    desc = """
        Listing des observation grace à l'utilisation de regex et d'un NER. 
        Pour le moment, extrait les locatisation anatomique avec :
            Precision : .84
            Recall : .84
            F-Score : .84
        """
    force_update=False
    
    def __init__(self, path=None) -> None:
        super().__init__()
        if path:
            # If path given load model by path
            self.logger.info(f"Start Loading {self.get_fullname()} model")
            self.load_model(path)
            self.logger.info(f"End Loading {self.get_fullname()} model")
        else:
            self.logger.info(f"Start Building {self.get_fullname()} model")
            # If not path given build model
            self.sections_patterns = ['intro', 'ctx', 'tech', 'obs', 'ccl']
            self.regex_patterns = {'identity':['gender', 'age'], 'medical':['suvmax', 'medobj_size']}
            self.treatment_ner_path = 'treatment_28_09_21'
            self.suv_ner_path = 'suv_28_09_21'
            self.build_model()
            self.logger.info(f"End Building {self.get_fullname()} model")

    def __call__(self, text, features) -> None:
        self.logger.info(f"Start features extraction for {self.get_fullname()} model")
        doc = self.nlp(text)
        self.add_feature(features, section_splitter.extract_sections(doc))
        self.add_feature(features, ('SUV_NER', extract_ents(doc, ['OBJ_LOC'])))
        self.add_feature(features, ('TREATMENT_NER', extract_ents(doc, ['T'])))
        self.add_feature(features, ('BASE_NER', extract_ents(doc, ['LOC', 'MISC', 'ORG', 'PER'])))
        self.add_feature(features, extract_sents(doc))
        for feature in regex_matcher.extract_matchs(doc):
            self.add_feature(features, feature)
        self.logger.info(f"End features extraction for {self.get_fullname()} model")
            
    def build_model(self) -> None:
        self.logger.info(f"Loading base model for {self.get_fullname()} model")
        self.nlp = spacy.load("fr_core_news_lg")

        self.logger.info(f"Add sbd component {self.get_fullname()} model")
        self.nlp.add_pipe("sbd", first=True)

        self.logger.info(f"Add sections_splitter component {self.get_fullname()} model")
        self.nlp.add_pipe("sections_splitter", config={"patterns": self.sections_patterns})

        self.logger.info(f"Add regex_matcher component {self.get_fullname()} model")
        self.nlp.add_pipe("regex_matcher", config={"patterns": self.regex_patterns})

        self.logger.info(f"Add treatment_ner component {self.get_fullname()} model")
        add_custom_ner(self.nlp, self.treatment_ner_path, 'treatment_ner')

        self.logger.info(f"Add suv_ner component {self.get_fullname()} model")
        add_custom_ner(self.nlp, self.suv_ner_path, 'suv_ner')

    def load_model(self, path) -> None:
        path = Path(path) if isinstance(path, str) else path
        config = Config().from_disk(path / self.get_fullname() / "config.cfg")
        lang_cls = spacy.util.get_lang_class(config["nlp"]["lang"])
        self.nlp = lang_cls.from_config(config)
        self.nlp.from_disk(path / self.get_fullname())

    def save_model(self, path) -> None:
        path = Path(path) if isinstance(path, str) else path
        path = path / self.get_fullname()
        self.nlp.to_disk(path)