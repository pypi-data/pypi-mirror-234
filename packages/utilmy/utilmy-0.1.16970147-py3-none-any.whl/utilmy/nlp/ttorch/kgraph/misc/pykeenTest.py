#%%
import os
import pandas as pd
import numpy as np
import pykeen
import torch

from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline
from pykeen.models import TransE,ERModel
from torch.optim import Adam
from pykeen.training import SLCWATrainingLoop, LCWATrainingLoop
from pykeen.evaluation import RankBasedEvaluator
from pykeen.nn.representation import LabelBasedTransformerRepresentation
print(pykeen.version.get_version())

#%%
train_path =os.path.join('pykeen_data','train_data.tsv')
test_path =os.path.join('pykeen_data','test_data.tsv')
val_path =os.path.join('pykeen_data','validation_data.tsv')
data_path = os.path.join('pykeen_data','data_kgf.tsv')


# data = TriplesFactory.from_path(path = data_path)
# training, testing, validation = data.split(ratios = [0.5,0.3])

training = TriplesFactory.from_path(train_path)

testing = TriplesFactory.from_path(test_path,
                                    entity_to_id=training.entity_to_id,
                                    relation_to_id=training.relation_to_id)
validation = TriplesFactory.from_path(val_path,
                                    entity_to_id=training.entity_to_id,
                                    relation_to_id=training.relation_to_id)

# entity_representations = LabelBasedTransformerRepresentation.from_triples_factory(training)
model = ERModel(triples_factory=training, interaction='distmult',
               # entity_representations=entity_representations
               entity_representations_kwargs = dict(embedding_dim=3, dropout=0.1),
               relation_representations_kwargs = dict(embedding_dim=3, dropout=0.1)
               )

# Pick an optimizer from Torch
optimizer = Adam(params=model.get_grad_params())

# Pick a training approach (sLCWA or LCWA)
training_loop = LCWATrainingLoop(
    model=model,
    triples_factory=training,
    optimizer=optimizer,
)

# %%
losses = training_loop.train(
                        triples_factory=training,
                        num_epochs=10,
                        checkpoint_name='myCheckpoint.pt',
                        checkpoint_frequency=5,
                        batch_size=256,
                        )

# Pick an evaluator
evaluator = RankBasedEvaluator()
# Get triples to test

mapped_triples = testing.mapped_triples
# Evaluate
results = evaluator.evaluate(
    model=model,
    mapped_triples=mapped_triples,
    batch_size=1024,
    additional_filter_triples=[
        training.mapped_triples,
        validation.mapped_triples,
    ],
)
torch.save(model, 'trained_model.pkl')

