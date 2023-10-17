import glob, os
import pandas as pd
import pyvista as pv

from simba.three_dimensions.mixins.plotting_mixin import PlottingMixin
from simba.three_dimensions.mixins.config_reader import ConfigReader
from simba.utils.checks import check_if_filepath_list_is_empty
from simba.utils.read_write import get_fn_ext, read_df
from simba.utils.printing import SimbaTimer

class PlotPoseInDirectory(PlottingMixin, ConfigReader):

    def __init__(self,
                 data_dir: str,
                 config_path: str,
                 settings: dict = None):

        ConfigReader.__init__(self, config_path=config_path, read_video_info=False)
        PlottingMixin.__init__(self)
        self.settings = settings
        self.data_files = glob.glob(data_dir + f'/*{self.file_type}')[1:2]
        check_if_filepath_list_is_empty(filepaths=self.data_files, error_msg=f'No {self.file_type} files found inside the {data_dir} directory.')

    def normalize_df(self,
                     df: pd.DataFrame,
                     max: int = 1000):

        max_x, min_x = df[self.x_cols].max().max(), df[self.x_cols].min().min()
        max_y, min_y = df[self.y_cols].max().max(), df[self.y_cols].min().min()
        max_z, min_z = df[self.z_cols].max().max(), df[self.z_cols].min().min()
        x_df, y_df, z_df = df[self.x_cols], df[self.y_cols], df[self.z_cols]
        x_df, y_df, z_df = (x_df - min_x) / (max_x - min_x), (y_df - min_y) / (max_y - min_y), (z_df - min_z) / (max_z - min_z)
        x_df *= max; y_df *= max; z_df *= max
        df = pd.concat([x_df, y_df, z_df, df[self.p_cols]], axis=1)[self.bp_headers]
        return df

    def run(self):
        for file_cnt, file_path in enumerate(self.data_files):
            video_timer = SimbaTimer(start=True)
            _, video_name, _ = get_fn_ext(filepath=file_path)
            data_df = read_df(file_path=file_path, file_type=self.file_type, has_index=True, check_multiindex=True)
            data_df.columns = self.bp_headers
            bp_arr = data_df.drop(self.p_cols, axis=1).values
            env = self.create_environment()
            video_save_path = os.path.join(self.frames_out_dir, video_name + '.mp4')
            self.create_video_file(environment=env, path=video_save_path, fps=25)
            self.add_stl(stl_path='/Users/simon/Desktop/envs/simba_dev/simba/assets/stl/grid_floor.stl', environment=env, scale=[2, 2, 2])
            self.initiate_mesh(environment=env, mesh=bp_arr[0].reshape(-1, 3), settings=self.settings)
            for i in range(bp_arr.shape[0]):
                print(f'Image {i+1}/{bp_arr.shape[0]} (video {file_cnt+1}/{len(file_path)}...)')
                env.camera.distance = 1000
                env.update_coordinates(bp_arr[i].reshape(-1, 3), render=False)
                env.show(auto_close=False)
                env.write_frame()
            env.close()

test = PlotPoseInDirectory(data_dir='/Users/simon/Desktop/envs/troubleshooting/anipose/project_folder/csv/input_csv',
                           config_path='/Users/simon/Desktop/envs/troubleshooting/anipose/project_folder/project_config.ini',
                           settings={'cmap': 'Accent', 'point_size': 10})

test.run()