class PipelineCtrl:
    def __init__(self, version, force_update=False) -> None:
        self.name = self.__class__.__name__
        self.version = version
        self.force_update=force_update
    
    def __call__(self, text) -> dict:
        return {}

    def get_fullname(self) -> str:
        return f'{self.name}_{self.version}'

    def add_feature(self, features : dict, newFeatures : dict) -> None: 
        # print(f'add_feature :\n*********\n{features}\n*********\n{newFeatures}\n*********')
        if features == None:
            return      
        fname, flist = newFeatures
        if fname not in features:
            features[fname] = {}
        features[fname][self.get_fullname()] = flist