from pathlib import Path
import spacy
import json, os
from .pipeline_ctrl import PipelineCtrl
from src.components import similarity
from src.helpers import DIM_KEYWORDS


class Dim(PipelineCtrl):
    name="Dim"
    version="0.1"
    desc = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"
    force_update=False

    def __init__(self) -> None:
        super().__init__()
        self.build_model()

    def __call__(self, text, features) -> None:
        doc = self.nlp(text)
        result = similarity.process_text(doc, self.keywords,[.8, .85, .75],
            [similarity.spacy_similarity, similarity.jaro_similarity,similarity.levenshtein_similarity])
        for r in result :
            self.add_feature(features, r)

    def build_model(self) -> None:
        self.nlp = spacy.load("fr_core_news_lg")
        self.keywords = [self.nlp(v) for v in DIM_KEYWORDS.values()]



    