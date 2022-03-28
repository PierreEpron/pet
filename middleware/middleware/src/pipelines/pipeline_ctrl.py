from re import I
from src.helpers import get_logger

class PipelineCtrl:
    name = ''
    version = ''
    desc = ''
    force_update = False

    def __init__(self) -> None:
        self.logger = get_logger()

    def __call__(self, text) -> dict:
        return {}

    @classmethod
    def get_fullname(self) -> str:
        return f'{self.name}_{self.version}'

    def add_feature(self, features : dict, newFeatures : dict) -> None: 
        fname, flist = newFeatures

        feature = self.add_or_create_feature(features, fname)
        source = self.add_or_create_source(feature['sources'])
        source['items'] = flist
        self.logger.info(f"Add {fname} from {self.get_fullname()} model")

    def add_or_create_feature(self, features, fname):
        feature = next(filter(lambda x: x['name'] == fname, features), False)
        if not feature:
            feature = {'name':fname, 'sources': []}
            features.append(feature)
        return feature
    
    def add_or_create_source(self, sources):
        source = next(filter(lambda x: x['name'] == self.get_fullname(), sources), False)
        if not source:
            source = {
                'name': self.get_fullname(),
                'type': 'model',
                'items': []
            }
            sources.append(source)
        return source
