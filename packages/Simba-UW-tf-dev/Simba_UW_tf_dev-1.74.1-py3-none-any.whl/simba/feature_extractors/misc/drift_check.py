import os
from typing import Union
from scipy.stats import f_oneway
from scipy.stats import t


from simba.mixins.train_model_mixin import TrainModelMixin
from simba.mixins.feature_extraction_supplement_mixin import FeatureExtractionSupplemental
from simba.mixins.config_reader import ConfigReader
from simba.utils.read_write import find_files_of_filetypes_in_directory
from simba.utils.checks import check_if_dir_exists
import pandas as pd


class DriftChecker(TrainModelMixin, ConfigReader, FeatureExtractionSupplemental):

    def __init__(self,
                 config_path: Union[str, os.PathLike],
                 train_data_dir: Union[str, os.PathLike],
                 new_data_dir: Union[str, os.PathLike]):

        TrainModelMixin.__init__(self)
        FeatureExtractionSupplemental.__init__(self)
        ConfigReader.__init__(self, config_path=config_path, read_video_info=False)
        check_if_dir_exists(in_dir=train_data_dir); check_if_dir_exists(in_dir=new_data_dir)
        train_data_paths = find_files_of_filetypes_in_directory(directory=train_data_dir, extensions=[f'.{self.file_type}'], raise_error=True)
        new_data_paths = find_files_of_filetypes_in_directory(directory=new_data_dir, extensions=[f'.{self.file_type}'], raise_error=True)
        self.train_df = self.read_all_files_in_folder_mp(file_paths=train_data_paths, file_type=self.file_type)
        self.new_df = self.read_all_files_in_folder_mp(file_paths=new_data_paths, file_type=self.file_type)
        self.features = [x for x in self.new_df.columns if x in self.train_df.columns]

    def run(self):
        t_results = pd.DataFrame(columns=['FEATURE', 'T_STATISTIC', 'P_VALUE', 'COHENS_D'])
        for x_name in self.features:
            t_stat, p_val = self.independent_samples_t(sample_1=self.train_df[x_name], sample_2=self.new_df[x_name])
            cohens_d = self.cohens_d(sample_1=self.train_df[x_name], sample_2=self.new_df[x_name])
            t_results.loc[len(t_results)] = [x_name, t_stat, p_val, cohens_d]



test = DriftChecker(config_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini',
                    train_data_dir='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/csv/targets_inserted',
                    new_data_dir='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/csv/targets_inserted')


test.run()
