import time

import numpy as np
from simba.utils.data import bucket_data
from typing_extensions import Literal
from numba import jit, typed
from numba import types, prange


@jit(nopython=True)
def _hist_1d(data: np.ndarray,
             bin_count: int,
             range: np.ndarray):
    """
    Jitted helper to compute 1D histograms with counts.

    .. note::
       For non-heuristic rules for bin counts and bin ranges, see ``simba.data.freedman_diaconis`` or simba.data.bucket_data``.

    :parameter np.ndarray data: 1d array containing feature values.
    :parameter int bins: The number of bins.
    :parameter: np.ndarray range: 1d array with two values representing minimum and maximum value to bin.
    """

    hist = np.histogram(data, bin_count, (range[0], range[1]))[0]
    return hist

@jit(nopython=True)
def _hbos_compute(data: np.ndarray, histograms: typed.Dict, histogram_edges: typed.Dict) -> np.ndarray:
    """
    Jitted helper to compute Histogram-based Outlier Score (HBOS) used by ``simba.mixins.statistics_mixin.Statistics.hbos``.

    :parameter np.ndarray data: 2d array with frames represented by rows and columns representing feature values.
    :parameter typed.Dict histograms: Numba typed.Dict with integer keys (representing order of feature) and 1d arrays as values representing observation bin counts.
    :parameter: typed.Dict histogram_edges: Numba typed.Dict with integer keys (representing order of feature) and 1d arrays as values representing bin edges.
    :return np.ndarray: Array of size data.shape[0] representing outlier scores, with higher values representing greater outliers.
    """
    results = np.full((data.shape[0]), np.nan)
    data = data.astype(np.float32)
    for i in prange(data.shape[0]):
        score = 0.0
        for j in prange(data.shape[1]):
            value, bin_idx = data[i][j], np.nan
            for k in np.arange(histogram_edges[j].shape[0], 0, -1):
                bin_max, bin_min = histogram_edges[j][k], histogram_edges[j][k-1]
                if (value <= bin_max) and (value > bin_min):
                    bin_idx = k
                    continue
            if np.isnan(bin_idx):
                bin_idx = 0
            score += -np.log(histograms[j][int(bin_idx) - 1] + 1e-10)
        results[i] = score
    return results


def hbos(data: np.ndarray,
         bucket_method: Literal['fd', 'doane', 'auto', 'scott', 'stone', 'rice', 'sturges', 'sqrt'] = 'auto'):

    """
    Jitted helper to compute Histogram-based Outlier Scores (HBOS).

    :parameter np.ndarray data: 2d array with frames represented by rows and columns representing feature values.
    :parameter Literal bucket_method: Estimator determining optimal bucket count and bucket width. Default: The maximum of the Sturges and Freedman-Diaconis estimators.
    :return np.ndarray: Array of size data.shape[0] representing outlier scores, with higher values representing greater outliers.


    :example:
    >>> sample_1 = np.random.random_integers(low=1, high=2, size=(100, 50)).astype(np.float64)
    >>> sample_2 = np.random.random_integers(low=7, high=20, size=(2, 50)).astype(np.float64)
    >>> data = np.vstack([sample_1, sample_2])
    >>> hbos(data=data)
    """

    min_vals, max_vals = np.min(data, axis=0), np.max(data, axis=0)
    data = (data - min_vals) / (max_vals - min_vals) * (1 - 0) + 0
    histogram_edges = typed.Dict.empty(key_type=types.int64, value_type=types.float64[:])
    histograms = typed.Dict.empty(key_type=types.int64, value_type=types.int64[:])
    for i in range(data.shape[1]):
        bin_width, bin_count = bucket_data(data=data, method=bucket_method)
        histograms[i] = _hist_1d(data=data, bin_count=bin_count, range=np.array([0, int(bin_width * bin_count)]))
        histogram_edges[i] = np.arange(0, 1+bin_width, bin_width).astype(np.float64)

    results = _hbos_compute(data=data, histograms=histograms, histogram_edges=histogram_edges)
    return results
