import glob, os
from copy import deepcopy
import pandas as pd

from simba.three_dimensions.mixins.config_reader import ConfigReader
from simba.utils.checks import (check_if_dir_exists, check_file_exist_and_readable, check_if_filepath_list_is_empty)
from simba.utils.read_write import read_df, get_fn_ext, write_df
from simba.utils.errors import BodypartColumnNotFoundError
from simba.utils.printing import SimbaTimer, stdout_success


N_CAMS_SUFFIX = '_ncams'
ERROR_SUFFIX = '_error'
FNUM = 'fnum'

class AniposeImporterCSV(ConfigReader):
    def __init__(self,
                 config_path: str,
                 data_dir: str):

        ConfigReader.__init__(self, config_path=config_path, read_video_info=False)
        check_file_exist_and_readable(file_path=config_path)
        check_if_dir_exists(in_dir=data_dir)
        self.anipose_file_paths = glob.glob(data_dir + f'/*{self.file_type}')
        check_if_filepath_list_is_empty(filepaths=self.anipose_file_paths, error_msg=f'No CSV files found inside the {data_dir} directory.')

    def reinsert_multi_idx_columns(self):
        multi_idx_cols = []
        for col_idx in range(len(self.out_df.columns)):
            multi_idx_cols.append(tuple(('IMPORTED_POSE', 'IMPORTED_POSE', self.out_df.columns[col_idx])))
        self.out_df.columns = pd.MultiIndex.from_tuples(multi_idx_cols, names=('scorer', 'bodypart', 'coords'))

    def run(self):
        for file_cnt, file_path in enumerate(self.anipose_file_paths):
            video_timer = SimbaTimer(start=True)
            _, video_name, _ = get_fn_ext(filepath=file_path)
            data_df = read_df(file_path=file_path, file_type=self.file_type, has_index=True, anipose_data=True)
            data_df = data_df[data_df.columns[~data_df.columns.str.endswith(N_CAMS_SUFFIX)]]
            data_df = data_df[data_df.columns[~data_df.columns.str.endswith(ERROR_SUFFIX)]]
            data_df = data_df.drop(FNUM, axis=1)
            self.out_df = deepcopy(data_df)
            if len(data_df.columns) != len(self.bp_headers):
                raise BodypartColumnNotFoundError(msg=f'The number of body-parts in data file {video_name} do not match the number of body-parts in your SimBA project. '
                      f'The number of of body-parts expected by your SimBA project is {int(len(self.bp_headers) / 4)}. '
                      f'The number of of body-parts contained in data file {video_name} is {(len(data_df.columns) / 4)}. '
                      f'Make sure you have specified the correct number of animals and body-parts in your project.', source=self.__class__.__name__)
            self.out_df.columns = self.bp_headers
            self.reinsert_multi_idx_columns()
            save_path = os.path.join(os.path.join(self.input_csv_dir, f'{video_name}.{self.file_type}'))
            write_df(df=self.out_df, save_path=save_path, file_type=self.file_type, multi_idx_header=True)
            video_timer.stop_timer()
            stdout_success(msg=f'Video {video_name} data imported...', elapsed_time=video_timer.elapsed_time_str, source=self.__class__.__name__)
        self.timer.stop_timer()
        stdout_success(msg='All ANIPOSE data files imported', elapsed_time=self.timer.elapsed_time_str, source=self.__class__.__name__)

# anipose_importer = AniposeImporterCSV(config_path='/Users/simon/Desktop/envs/troubleshooting/anipose/project_folder/project_config.ini',
#                                       data_dir='/Users/simon/Desktop/envs/troubleshooting/anipose/anipose_data')
# anipose_importer.run()
