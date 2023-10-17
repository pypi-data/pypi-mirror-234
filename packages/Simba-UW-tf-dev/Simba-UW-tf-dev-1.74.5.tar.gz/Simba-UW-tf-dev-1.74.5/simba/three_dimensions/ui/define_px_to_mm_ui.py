import pyvista as pv
from simba.three_dimensions.mixins.config_reader import ConfigReader
from simba.three_dimensions.mixins.plotting_mixin import PlottingMixin
from simba.utils.checks import check_file_exist_and_readable
from simba.utils.read_write import read_df

class Pixels2Millimeters(ConfigReader, PlottingMixin):

    def __init__(self,
                 config_path: str,
                 data_path: str):

        ConfigReader.__init__(self, config_path=config_path, read_video_info=False)
        PlottingMixin.__init__(self)
        check_file_exist_and_readable(file_path=data_path)
        self.data_df = read_df(file_path=data_path, file_type=self.file_type, check_multiindex=True)
        self.data_df.columns = self.bp_headers
        self.bp_arr = self.reshape_df_for_plotting(df=self.data_df.drop(self.p_cols, axis=1).astype(int))

    def run(self):
        env = self.create_environment(off_screen=False)
        env.enable_joystick_style()
        self.initiate_mesh(environment=env, mesh=self.bp_arr[0])
        env.enable_point_picking(callback=self.point_picking_callback, show_message='')
        env.add_key_event('v', self.froward_one_frame_callback)
        env.add_key_event('b', self.froward_ten_frame_callback)
        env.add_key_event('n', self.froward_hundred_frame_callback)
        self.store_array(data=self.bp_arr[0]); self.store_bp_names(bp_names=self.bp_col_names); self.store_environment(environment=env)
        env.show()







test = Pixels2Millimeters(config_path='/Users/simon/Desktop/envs/troubleshooting/anipose/project_folder/project_config.ini',
                          data_path='/Users/simon/Desktop/envs/troubleshooting/anipose/project_folder/csv/input_csv/2019-08-02-vid01.csv')
test.run()
