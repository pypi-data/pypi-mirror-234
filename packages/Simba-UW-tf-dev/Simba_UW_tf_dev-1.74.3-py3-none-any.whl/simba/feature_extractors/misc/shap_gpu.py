import shap
import pandas
import numpy as np
from simba.mixins.train_model_mixin import TrainModelMixin

model = TrainModelMixin().read_pickle(file_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/models/generated_models/Attack.sav')

data = np.random.random((3,587))

explainer = shap.explainers.GPUTree(model=model, model_output='raw', feature_perturbation='tree_path_dependent')
explainer(X=data)