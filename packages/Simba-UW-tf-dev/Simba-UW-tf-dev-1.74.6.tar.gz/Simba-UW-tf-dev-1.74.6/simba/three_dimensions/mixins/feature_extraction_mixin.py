from numba import jit, prange
import numpy as np
from scipy.spatial import ConvexHull
import pandas as pd

class FeatureExtractionMixin(object):



    @staticmethod
    @jit(nopython=True, cache=True)
    def framewise_euclidean_distance(location_1: np.ndarray,
                                     location_2: np.ndarray,
                                     px_per_mm: float,
                                     centimeter: bool = False) -> np.ndarray:
        """
        Jitted helper finding frame-wise distances between two moving locations in millimeter or centimeter.

        :parameter ndarray location_1: 2D array of size len(frames) x 3.
        :parameter ndarray location_1: 2D array of size len(frames) x 3.
        :parameter float px_per_mm: The pixels per millimeter in the video.
        :parameter bool centimeter: If true, the value in centimeters is returned. Else the value in millimeters.

        :return np.ndarray: 1D array of size location_1.shape[0]

        """
        # if not px_per_mm and centimeter:
        #     raise InvalidInputError(msg='To calculate centimeters, provide a pixel per millimeter value')
        results = np.full((location_1.shape[0]), np.nan)
        for i in prange(location_1.shape[0]):
            results[i] = np.linalg.norm(location_1[i] - location_2[i]) / px_per_mm
        if centimeter and px_per_mm:
            results = results / 10
        return results

    @staticmethod
    @jit(nopython=True, fastmath=True)
    def angle3pt_serialized(location_1: np.ndarray,
                            location_2: np.ndarray,
                            location_3: np.ndarray) -> np.ndarray:
        """
        Jitted helper for frame-wise 3-point angles.

        :parameter ndarray location_1: 2D numerical array with frame number on x and [ax, ay, az] on y.
        :parameter ndarray location_2: 2D numerical array with frame number on x and [bx, by, bz] on y.
        :parameter ndarray location_3: 2D numerical array with frame number on x and [cx, cy, cz] on y.
        :return ndarray: 1d float numerical array of size data.shape[0] with angles in degrees.

        :examples:
        """

        results = np.full((location_1.shape[0]), 0.0)
        for i in prange(location_1.shape[0]):
            ba, bc = location_1[i] - location_2[i], location_3[i] - location_2[i]
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            angle = np.arccos(cosine_angle)
            results[i] = np.degrees(angle)
        return results

    def df_to_array(self,
                    df: pd.DataFrame) -> np.ndarray:

        data = df.values
        return np.reshape(data, (-1, int(data.shape[1] / 3), 3))

    @staticmethod
    def create_shifted_df(df: pd.DataFrame) -> pd.DataFrame:
        """
        Create dataframe including duplicated shifted (1) columns with ``_shifted`` suffix.

        :parameter pd.DataFrame df
        :return pd.DataFrame: Dataframe including original and shifted columns.

        :example:
        >>> df = pd.DataFrame(np.random.randint(0,100,size=(3, 1)), columns=['Feature_1'])
        >>> FeatureExtractionMixin.create_shifted_df(df=df)
        >>>             Feature_1  Feature_1_shifted
        >>>    0         76               76.0
        >>>    1         41               76.0
        >>>    2         89               41.0

        """
        data_df_shifted = df.shift(periods=1)
        data_df_shifted = data_df_shifted.combine_first(df).add_suffix('_shifted')
        return pd.concat([df, data_df_shifted], axis=1, join='inner').reset_index(drop=True)

    @staticmethod
    def volume(points: np.ndarray, pixels_per_mm: float) -> float:
        return ConvexHull(points).volume / pixels_per_mm





