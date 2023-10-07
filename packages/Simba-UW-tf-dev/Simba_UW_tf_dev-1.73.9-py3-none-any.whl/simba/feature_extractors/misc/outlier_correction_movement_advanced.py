__author__ = "Simon Nilsson"

import os, glob
import pandas as pd
import numpy as np
from typing import Union
from numba import jit, prange
from simba.mixins.config_reader import ConfigReader
from simba.utils.read_write import read_df, write_df, get_fn_ext, read_config_entry
from simba.utils.printing import stdout_success, SimbaTimer
from simba.utils.enums import ConfigKey, Dtypes
from simba.mixins.feature_extraction_mixin import FeatureExtractionMixin
from simba.utils.read_write import find_files_of_filetypes_in_directory
from simba.utils.errors import NoFilesFoundError

class OutlierCorrecterMovementAdvanced(ConfigReader, FeatureExtractionMixin):
    def __init__(self,
                 config_path: Union[str, os.PathLike],
                 input_dir:  Union[str, os.PathLike],
                 type: str,
                 settings: dict):

        ConfigReader.__init__(self, config_path=config_path)
        self.data_files = find_files_of_filetypes_in_directory(directory=input_dir, extensions=['.' +self.file_type])
        if len(self.data_files) == 0:
            raise NoFilesFoundError(msg=f'No data of filetype {input_dir} for in directory {self.file_type}')
        self.settings, self.type = settings, type

    def fix_settings_for_animal_input(self):
        new_settings = {}
        for animal_name, animal_bps in self.animal_bp_dict.items():
            print(animal_name)
            if animal_name not in new_settings.keys():
                new_settings[animal_name] = {}
            for body_part in animal_bps['X_bps']:
                new_settings[animal_name][body_part] = self.settings[animal_name]
        self.settings = new_settings


    def run(self):
        if self.type == 'animal':
            self.fix_settings_for_animal_input()


        self.log = pd.DataFrame(columns=['VIDEO', 'ANIMAL', 'BODY-PART', 'CORRECTION COUNT', 'CORRECTION PCT'])
        for file_cnt, file_path in enumerate(self.data_files):
            video_timer = SimbaTimer(start=True)
            _, self.video_name, _ = get_fn_ext(file_path)
            print('Processing video {}. Video {}/{}...'.format(self.video_name, str(file_cnt+1), str(len(self.data_files))))
            self.data_df = read_df(file_path, self.file_type, check_multiindex=True)
            self.data_df = self.insert_column_headers_for_outlier_correction(data_df=self.data_df, new_headers=self.bp_headers, filepath=file_path)
            self.data_df_combined = self.create_shifted_df(df=self.data_df)
            for animal, animal_bps in self.settings.items():



    #         self.animal_criteria = {}
    #         for animal_name, animal_bps in self.outlier_bp_dict.items():
    #             animal_bp_distances = np.sqrt((self.data_df[animal_bps['bp_1'] + '_x'] - self.data_df[animal_bps['bp_2'] + '_x']) ** 2 + (self.data_df[animal_bps['bp_1'] + '_y'] - self.data_df[animal_bps['bp_2'] + '_y']) ** 2)
    #             self.animal_criteria[animal_name] = animal_bp_distances.mean() * self.criterion
    #         self.__outlier_replacer()
    #         write_df(df=self.data_df, file_type=self.file_type, save_path=save_path)
    #         video_timer.stop_timer()
    #         print(f'Corrected movement outliers for file {self.video_name} (elapsed time: {video_timer.elapsed_time_str}s)...')
    #     self.__save_log_file()
    #
    # def __save_log_file(self):
    #     self.log_fn = os.path.join(self.logs_path, 'Outliers_movement_{}.csv'.format(self.datetime))
    #     self.log.to_csv(self.log_fn)
    #     self.timer.stop_timer()
    #     stdout_success(msg='Log for corrected "movement outliers" saved in project_folder/logs', elapsed_time=self.timer.elapsed_time_str)
    #
    # @staticmethod
    # @jit(nopython=True)
    # def __corrector(data=np.ndarray, criterion=float):
    #
    #     results, current_value, cnt = np.full(data.shape, np.nan), data[0, :], 0
    #     for i in range(data.shape[0]):
    #         dist = abs(np.linalg.norm(current_value - data[i, :]))
    #         if dist <= criterion:
    #             current_value = data[i, :]
    #             cnt += 1
    #         results[i, :] = current_value
    #     return results, cnt
    #
    # def __outlier_replacer(self):
    #     for animal_name, animal_body_parts in self.animal_bp_dict.items():
    #         for (bp_x_name, bp_y_name) in zip(animal_body_parts['X_bps'], animal_body_parts['Y_bps']):
    #             vals, cnt = self.__corrector(data=self.data_df[[bp_x_name, bp_y_name]].values, criterion=self.animal_criteria[animal_name])
    #             df = pd.DataFrame(vals, columns=[bp_x_name, bp_y_name])
    #             self.data_df.update(df)
    #             self.log.loc[len(self.log)] = [self.video_name, animal_name, bp_x_name[:-2], cnt, round(cnt/len(df), 6)]
    #
    #
    #

settings = {'Simon': 2, 'JJ': 3}


test = OutlierCorrecterMovementAdvanced(config_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini',
                                        input_dir='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/csv/input_csv',
                                        type='animal',
                                        settings=settings)
test.run()


