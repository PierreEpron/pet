from pathlib import Path
import spacy
from thinc.api import Config
from src.pipelines.pipeline_ctrl import PipelineCtrl
from src.components import section_splitter
from src.components import regex_matcher
from src.components import pysbd_sentence_boundaries
from src.helpers import extract_sents

class Alpha(PipelineCtrl):
    def __init__(self) -> None:
        super().__init__(version="0.1", force_update=True)
        self.desc = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"
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
        self.nlp = spacy.load("fr_core_news_lg")
        self.nlp.add_pipe("sbd", first=True)
        self.nlp.add_pipe("sections_splitter", config={"patterns": self.sections_patterns})
        self.nlp.add_pipe("regex_matcher", config={"patterns": self.regex_patterns})

    def load_model(self, path) -> None:
        path = Path(path) if isinstance(path, str) else path
        config = Config().from_disk(path / self.get_fullname() / "config.cfg")
        lang_cls = spacy.util.get_lang_class(config["nlp"]["lang"])
        self.nlp = lang_cls.from_config(config)
        self.nlp.from_disk(path / self.get_fullname())

    def save_model(self, path) -> None:
        path = Path(path) if isinstance(path, str) else path
        self.nlp.to_disk(path / self.get_fullname())