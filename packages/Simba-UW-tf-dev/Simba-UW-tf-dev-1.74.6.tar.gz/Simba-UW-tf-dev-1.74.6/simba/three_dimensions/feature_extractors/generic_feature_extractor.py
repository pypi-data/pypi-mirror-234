import os.path
from itertools import combinations, product
from copy import deepcopy
from joblib import Parallel, delayed
import numpy as np
from numba import jit, prange

from simba.three_dimensions.mixins.config_reader import ConfigReader
from simba.three_dimensions.mixins.feature_extraction_mixin import FeatureExtractionMixin
from simba.utils.checks import check_if_filepath_list_is_empty, check_minimum_roll_windows
from simba.utils.read_write import get_fn_ext, read_video_info, read_df, write_df
from simba.utils.enums import Options
from simba.utils.printing import stdout_success, SimbaTimer

class GenericFeatureExtractor(ConfigReader, FeatureExtractionMixin):
    def __init__(self,
                 config_path: str):

        ConfigReader.__init__(self, config_path=config_path, read_video_info=True)
        FeatureExtractionMixin.__init__(self)
        check_if_filepath_list_is_empty(self.outlier_corrected_paths, error_msg=f'{self.outlier_corrected_movement_dir} directory is empty')
        self.roll_windows_values = check_minimum_roll_windows(Options.ROLLING_WINDOW_DIVISORS.value, self.video_info_df['fps'].min())



    @staticmethod
    def rolling_window_aggregate_statistics(data: np.ndarray,
                                            method: str,
                                            window: int) -> np.ndarray:
        results = np.full((data.shape[0]), 0.0)
        left_pointer = 0
        for right_pointer in prange(window, data.shape[0]):
            if method == 'sum':
                results[right_pointer] = np.sum(data[left_pointer:right_pointer+1])
            if method == 'mean':
                results[right_pointer] = np.mean(data[left_pointer:right_pointer+1])
            left_pointer +=1; right_pointer+=1
        return results

    @staticmethod
    def rolling_peak_cnt(data: np.ndarray, window: int) -> np.ndarray:
        results = np.full((data.shape[0]), 0.0)
        left_pointer = 0
        for right_pointer in prange(window, data.shape[0]):
            peak_cnt = 0
            sliced_data = data[left_pointer:right_pointer + 1]
            if sliced_data[0] > sliced_data[1]: peak_cnt += 1
            if sliced_data[-1] > sliced_data[-2]: peak_cnt += 1
            for i in prange(1, sliced_data.shape[0]-1):
                if sliced_data[i-1] <  sliced_data[i] > sliced_data[i+1]:
                    peak_cnt += 1
            results[right_pointer] = peak_cnt
            left_pointer += 1; right_pointer += 1
        return results

    @staticmethod
    def rolling_ttests(data: np.ndarray, stride: int) -> np.ndarray:
        results = np.full((data.shape[0]), 0.0)
        data = np.split(data, np.arange(stride, data.shape[0], stride))
        for i in prange(1, len(data)):
            x1, x2 = np.mean(data[i-1]), np.mean(data[i])
            s1, s2 = np.std(data[i - 1]), np.std(data[i])
            n1, n2 = data[i - 1].shape[0], data[i].shape[0]
            results[i*stride: (i*stride) + stride] = (x1-x2) / np.sqrt((np.square(s1) / n1) + (np.square(s2) / n2))

        return results

    def run(self):
        for file_cnt, file_path in enumerate(self.outlier_corrected_paths):
            video_name = get_fn_ext(filepath=file_path)[1]
            video_timer = SimbaTimer(start=True)
            save_path = os.path.join(self.features_dir, video_name + f'.{self.file_type}')
            _, px_per_mm, fps = read_video_info(vid_info_df=self.video_info_df, video_name=video_name)
            data_df = read_df(file_path=file_path, file_type=self.file_type, check_multiindex=True)
            data_df.columns = self.bp_headers
            shifted_df = self.create_shifted_df(df=data_df)
            self.results = deepcopy(data_df)

            roll_windows = []
            for window in self.roll_windows_values: roll_windows.append(int(fps / window))
            roll_windows = roll_windows[0:1]

            for bps in combinations(self.body_parts_lst, 2):
                bp_one, bp_two = data_df[[f'{bps[0]}_x', f'{bps[0]}_y', f'{bps[0]}_z']].values, data_df[[f'{bps[1]}_x', f'{bps[1]}_y', f'{bps[1]}_z']].values
                self.results[f'Euclidean_distance_{bps[0]}_{bps[1]}_mm'] = self.framewise_euclidean_distance(location_1=bp_one, location_2=bp_two, px_per_mm=px_per_mm)

            for bps in combinations(self.body_parts_lst, 3):
                bp_one, bp_two = data_df[[f'{bps[0]}_x', f'{bps[0]}_y', f'{bps[0]}_z']].values, data_df[[f'{bps[1]}_x', f'{bps[1]}_y', f'{bps[1]}_z']].values
                bp_three = data_df[[f'{bps[2]}_x', f'{bps[2]}_y', f'{bps[2]}_z']].values
                self.results[f'Three_point_angle_{bps[0]}_{bps[1]}_{bps[2]}_degrees'] = self.angle3pt_serialized(location_1=bp_one, location_2=bp_two, location_3=bp_three)

            data_arr = self.df_to_array(df=data_df.drop(self.p_cols, axis=1))
            self.results['volume'] = np.round(Parallel(n_jobs=self.cpu_cnt, verbose=2, backend="loky")(delayed(self.volume)(x, px_per_mm) for x in data_arr), 2) / px_per_mm

            for bp in self.body_parts_lst:
                bp_loc_one, bp_loc_two = shifted_df[[f'{bp}_x_shifted', f'{bp}_y_shifted', f'{bp}_z_shifted']].values, data_df[[f'{bp}_x', f'{bp}_y', f'{bp}_z']].values
                self.results[f'{bp}_movement_single_frame_mm'] = np.round(self.framewise_euclidean_distance(location_1=bp_loc_one, location_2=bp_loc_two, px_per_mm=px_per_mm), 4)

            for (window, bp) in list(product(roll_windows, self.body_parts_lst)):
                data = self.results[f'{bp}_movement_single_frame_mm']
                self.results[f'{bp}_movement_sum_window_size_{window}'] = self.rolling_window_aggregate_statistics(data=data, method='sum', window=window)
                self.results[f'{bp}_movement_mean_window_size_{window}'] = self.rolling_window_aggregate_statistics(data=data, method='mean', window=window)

            for feature in [x for x in self.results.columns if '_movement_single_frame_mm' in x]:
                data = self.results[feature].values
                self.results[f'peak_cnt_{feature}'] = self.rolling_peak_cnt(data=data, window=int(fps))

            for feature in [x for x in self.results.columns if '_movement_single_frame_mm' in x]:
                data = self.results[feature].values
                self.results[f'{feature}_t_statistics_by_second'] = self.rolling_ttests(data=data, stride=int(fps))

            write_df(df=self.results, file_type=self.file_type, save_path=save_path)
            video_timer.stop_timer()
            stdout_success(msg=f'Feature extraction for video {video_name} complete', elapsed_time=video_timer.elapsed_time_str, source=self.__class__.__name__)

test = GenericFeatureExtractor(config_path='/Users/simon/Desktop/envs/troubleshooting/anipose/project_folder/project_config.ini')
test.run()