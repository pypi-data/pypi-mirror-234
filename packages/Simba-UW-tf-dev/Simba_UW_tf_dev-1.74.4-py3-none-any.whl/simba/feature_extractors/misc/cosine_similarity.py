import time
from typing import Union
import numpy as np
from sklearn.neighbors import LocalOutlierFactor

def local_outlier_factor(data: np.ndarray,
                         k: Union[int, float] = 5,
                         contamination: float = 1e-10) -> np.ndarray:

    if isinstance(k, float):
        k = int(data.shape[0] * k)
    lof_model = LocalOutlierFactor(n_neighbors=k, contamination=contamination)
    _ = lof_model.fit_predict(data)
    return -lof_model.negative_outlier_factor_


#results = local_outlier_factor(data=data, k=10)
#print(results)

np.random.seed(42)



data = np.random.normal(loc=45, scale=1, size=100).astype(np.float32)
for i in range(5): data = np.vstack([data, np.random.normal(loc=45, scale=1, size=100).astype(np.float32)])
for i in range(2): data = np.vstack([data, np.random.normal(loc=90, scale=1, size=100).astype(np.float32)])
local_outlier_factor(data=data, k=5).astype(np.float32)



# lof_model = LocalOutlierFactor(n_neighbors=50, contamination=1e-10)
# start = time.time()
# outlier_labels = lof_model
# lof_scores = -lof_model.negative_outlier_factor_
# print(time.time() - start)
# #print(results, lof_scores)
