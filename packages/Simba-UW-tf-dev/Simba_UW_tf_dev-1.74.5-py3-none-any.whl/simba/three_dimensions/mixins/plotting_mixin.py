import numpy as np
import pandas as pd
import pyvista as pv
from collections import deque

from simba.utils.errors import NoDataError


class PlottingMixin():

    def reshape_df_for_plotting(self,
                                df: pd.DataFrame) -> np.ndarray:

        data = df.values
        self.data = np.reshape(data, (-1, int(data.shape[1] / 3), 3))
        return self.data

    @staticmethod
    def add_stl(stl_path: str,
                environment: pv.Plotter,
                scale: None):
        poly_data = pv.PolyData(stl_path)
        if scale:
            poly_data.scale(scale, inplace=True)

        return environment.add_mesh(poly_data, opacity=0.5, point_size=5)


    @staticmethod
    def create_environment(bg_clr_bottom: str = 'black',
                           bg_clr_top: str = 'skyblue',
                           off_screen: bool = True):

        environment = pv.Plotter(lighting='light_kit',
                                 polygon_smoothing=True,
                                 off_screen=off_screen)
        environment.set_background(bg_clr_bottom, top=bg_clr_top)
        environment.enable_eye_dome_lighting()
        return environment


    @staticmethod
    def create_video_file(environment: pv.Plotter,
                          path: str,
                          fps: int,
                          quality: int = 10):
        environment.open_movie(path, quality=quality, framerate=fps)

    def initiate_mesh(self,
                      environment: pv.Plotter,
                      mesh: np.ndarray,
                      settings: dict = {'point_size': 30, 'cmap': 'Accent'}):
        self.current_frm = 0
        clr_scalars = np.linspace(0, mesh.shape[0], mesh.shape[0])
        return environment.add_mesh(mesh, color='salmon', scalars=clr_scalars, render_points_as_spheres=True, point_size=settings['point_size'], cmap=settings['cmap'], ambient=0.5, categories=True, name='Animal_1')

    def store_array(self,
                    data: np.ndarray):
        self.data_array = data


    def store_bp_names(self,
                       bp_names: list):
        self.bp_names = bp_names

    def store_environment(self,
                          environment: pv.Plotter):
        self.environment = environment

    def point_picking_callback(self,
                               point_id: np.ndarray):

        if not hasattr(self, 'bp_names') and not hasattr(self, 'data_array'):
            raise NoDataError(msg='Define body-part names and data first', source=self.__class__.__name__)

        if not hasattr(self, 'body_part_refs'):
            self.body_part_refs = deque(maxlen=2)

        bp_idx = np.where(((self.data_array[:, 0] == point_id[0]) & (self.data_array[:, 1] == point_id[1]) & ((self.data_array[:, 2] == point_id[2]))))[0][0]
        body_part_name = self.bp_names[bp_idx][:-4]
        self.body_part_refs.appendleft({body_part_name: point_id})

        for cnt, (bp, position) in enumerate(zip(self.body_part_refs, ['upper_left', 'lower_left'])):
            text = f'{list(bp.keys())[0]}: {list(bp.values())[0]}'
            self.environment.add_text(text=text, color='white', font_size=14, font='arial', shadow=False, position=position, name=str(cnt))

        if len(self.body_part_refs) == 2:
            bp_loc_1, bp_loc_2 = list(self.body_part_refs[0].values())[0], list(self.body_part_refs[1].values())[0]
            line = pv.Line(bp_loc_1, bp_loc_2)
            self.environment.add_mesh(line, color="white", line_width=10, name='line')

    def update_frm(self,
                   move_frame: int):
        self.current_frm = self.current_frm + move_frame
        self.environment.update_coordinates(self.data[self.current_frm], render=True)

    def froward_one_frame_callback(self):
        self.update_frm(move_frame=1)

    def froward_ten_frame_callback(self):
        self.update_frm(move_frame=10)

    def froward_hundred_frame_callback(self):
        self.update_frm(move_frame=10)