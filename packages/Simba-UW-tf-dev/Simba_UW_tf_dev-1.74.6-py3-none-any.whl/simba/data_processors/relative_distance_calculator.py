from typing import Union, Tuple, List

import os
import pandas as pd
import numpy as np
from itertools import combinations, product
from simba.mixins.config_reader import ConfigReader
from simba.mixins.feature_extraction_mixin import FeatureExtractionMixin
from simba.utils.errors import NoDataError
from simba.utils.read_write import read_df, get_fn_ext



class RelativeDistanceCalculator(ConfigReader, FeatureExtractionMixin):

    def __init__(self,
                 config_path: Union[str, os.PathLike],
                 time_windows_s: np.ndarray = np.array([0.2, 0.4, 0.8, 1.6])):

        ConfigReader.__init__(self, config_path=config_path, read_video_info=True)
        FeatureExtractionMixin.__init__(self)
        if len(self.feature_file_paths) == 0:
            raise NoDataError(msg=f'No data files found in {self.features_dir}')
        self.time_windows = time_windows_s

    def run(self):
        for file_cnt, file_path in enumerate(self.feature_file_paths):
            df = read_df(file_path=file_path, file_type=self.file_type)
            _, video_name, _ = get_fn_ext(filepath=file_path)
            _, px_per_mm, fps = self.read_video_info(video_name=video_name)
            print(px_per_mm, fps)
            animal_combinations = list(combinations(list(self.animal_bp_dict.keys()), 2))
            for animal_comb in animal_combinations:
                bp_combs = list(product(self.animal_bp_dict[animal_comb[0]]['X_bps'], self.animal_bp_dict[animal_comb[1]]['X_bps']))
                for bp_comb in bp_combs:
                    bp_names = (bp_comb[0][:-2], bp_comb[1][:-2])
                    location_1, location_2 = df[[f'{bp_names[0]}_x', f'{bp_names[0]}_y']].values.astype('float32'), df[[f'{bp_names[1]}_x', f'{bp_names[1]}_y']].values.astype('float32')
                    self.change_in_bodypart_euclidean_distance(location_1=location_1, location_2=location_2, fps=fps, px_per_mm=px_per_mm, time_windows=self.time_windows)


                # first_animal_bps, second_animal_bps = [], []
                # for bp in self.animal_bp_dict[animal_combination[0]]['X_bps']: first_animal_bps.extend(([f'{bp[:-2]}_x', f'{bp[:-2]}_y']))
                # for bp in self.animal_bp_dict[animal_combination[1]]['X_bps']: second_animal_bps.extend(([f'{bp[:-2]}_x', f'{bp[:-2]}_y']))
                # first_animal_df, second_animal_df = df[first_animal_bps].astype(int), df[second_animal_bps].astype(int)
                #




                # first_animal_array, second_animal_array = df[first_animal_bps].values.reshape(len(df), -1, 2), df[second_animal_bps].values.reshape(len(df), -1, 2)
                # print(second_animal_array)


                #print(first_animal_array)

            # for animal_name, animal_body_parts in self.animal_bp_dict.items():
            #     animal_bp_col_names = []
            #
            #


test = RelativeDistanceCalculator(config_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini',
                                  time_windows_s=np.array([0.2, 0.4]))
test.run()







