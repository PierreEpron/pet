import timeit
from src.pipelines.alpha import Alpha
import pandas as pd
import random

N = 1
PIPELINE = Alpha()
DF = pd.read_csv('../../../devia_1.csv', sep='\t', encoding='utf-8')
FEATURES = []

def setup():
    from __main__ import PIPELINE
    from __main__ import DF
    from __main__ import FEATURES

def stmt():
    FEATURES = []
    PIPELINE(DF["COMPTE_RENDU"][random.randint(0, len(DF)-1)], FEATURES)

t = timeit.timeit(setup=setup, stmt=stmt, number=N)
print(f"Total time for {N} : {t}, Mean time : {t/N}")

PIPELINE(DF["COMPTE_RENDU"][random.randint(0, len(DF)-1)], FEATURES)
print(FEATURES)

print(PIPELINE.nlp.pipe_names)
PIPELINE.save_model('models')
PIPELINE.load_model('models')
print(PIPELINE.nlp.pipe_names)