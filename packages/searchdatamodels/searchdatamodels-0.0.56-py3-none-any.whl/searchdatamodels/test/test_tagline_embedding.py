import sys
import os
sys.path.append(os.getcwd())
from searchdatamodels.tagline_embedding import *
import unittest
import time
import wandb

os.environ["WANDB_API_KEY"]="b735d9d48a34be4fddbf371c8615d3b9caeccd78"

class TaglineEmbeddingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        run = wandb.init(project="sentence_embedding_unit_test")
    
    @classmethod
    def tearDownClass(cls):
        wandb.finish()

    def test_create_embedding(self):
        columns=["tagline", "model_name", "time"]
        data=[]
        for text in ["architect at the eiffel tower", "diplomat at the united nations"]:
            for model_name in SENTENCE_EMBEDDING_MODELS:
                start=time.time()
                create_embedding(text, model_name)
                end=time.time()
                data.append([text, model_name, str(end-start)])
        table =  wandb.Table(data=data, columns=columns)
        wandb.log({"embedding times": table})