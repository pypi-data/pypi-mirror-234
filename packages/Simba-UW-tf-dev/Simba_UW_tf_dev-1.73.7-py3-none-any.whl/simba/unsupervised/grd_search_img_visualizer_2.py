import numpy as np
import matplotlib.pyplot as plt
from simba.unsupervised.misc import check_directory_exists
import glob
import pandas as pd
from simba.misc_tools import (check_file_exist_and_readable,
                              get_video_meta_data,
                              find_all_videos_in_directory,
                              check_multi_animal_status,
                              SimbaTimer,
                              check_if_filepath_list_is_empty)
from simba.unsupervised.enums import Clustering, Unsupervised
from simba.mixins.unsupervised_mixin import UnsupervisedMixin
from simba.drop_bp_cords import getBpNames, create_body_part_dictionary, createColorListofList
from simba.read_config_unit_tests import read_config_file, read_config_entry, read_project_path_and_file_type
from simba.enums import Paths, Formats, ReadConfig, Dtypes
import os
import warnings
import cv2


class GridSearchClusterVisualizer(UnsupervisedMixin):
    def __init__(self,
                 model_dir: str,
                 save_dir: str,
                 settings: dict):

        super().__init__()
        check_directory_exists(save_dir)
        self.save_dir, self.settings, self.model_dir = save_dir, settings, model_dir
        check_directory_exists(save_dir)
        check_directory_exists(model_dir)
        self.data_path = glob.glob(model_dir + '/*.pickle')
        check_if_filepath_list_is_empty(filepaths=self.data_path, error_msg=f'SIMBA ERROR: No pickle files in {model_dir}')

    def run(self):
        data = self.read_pickle(self.model_dir)
        for k, v in data.items():
            self.check_key_exist_in_object(object=v, key=Clustering.CLUSTER_MODEL.value)
        for k, v in data.items():
            labels = v[Clustering.CLUSTER_MODEL.value][Unsupervised.MODEL.value].labels_.reshape(-1, 1).astype(np.int8)
            embeddings = pd.DataFrame(v[Unsupervised.DR_MODEL.value][Unsupervised.MODEL.value].embedding_, columns=['X', 'Y'])


            self.img_data[k]['DATA'] = pd.DataFrame(data, columns=['X', 'Y', 'CLUSTER'])

    # def create_datasets(self):
    #     self.img_data = {}
    #     print('Retrieving models for visualization...')
    #     for k, v in self.clusterers.items():
    #         self.img_data[k] = {}
    #         self.img_data[k]['categorical_legends'] = set()
    #         self.img_data[k]['continuous_legends'] = set()
    #         embedder = v['EMBEDDER']
    #         cluster_data = v['MODEL'].labels_.reshape(-1, 1).astype(np.int8)
    #         embedding_data = embedder['MODEL'].embedding_
    #         data = np.hstack((embedding_data, cluster_data))
    #         self.img_data[k]['DATA'] = pd.DataFrame(data, columns=['X', 'Y', 'CLUSTER'])
    #         self.img_data[k]['HASH'] = v['HASH']
    #         self.img_data[k]['EMBEDDER'] = embedder
    #         self.img_data[k]['CLUSTERER_NAME'] = v['NAME']
    #         self.img_data[k]['categorical_legends'].add('CLUSTER')
    #
    #     if self.settings['HUE']:
    #         for hue_id, hue_settings in self.settings['HUE'].items():
    #             field_type, field_name = hue_settings['FIELD_TYPE'], hue_settings['FIELD_NAME']
    #             for k, v in self.img_data.items():
    #                 embedder = v['EMBEDDER']
    #                 if not 'categorical_legends' in self.img_data[k].keys():
    #                     self.img_data[k]['categorical_legends'] = set()
    #                     self.img_data[k]['continuous_legends'] = set()
    #                 if (field_type == 'CLASSIFIER'):
    #                     self.img_data[k]['categorical_legends'].add(field_name)
    #                 if (field_type == 'VIDEO NAMES'):
    #                     self.img_data[k]['categorical_legends'].add(field_type)
    #                 elif (field_type == 'CLASSIFIER PROBABILITY') or (field_type == 'START FRAME'):
    #                     if field_name != 'None' and field_name != '':
    #                         self.img_data[k]['continuous_legends'].add(field_name)
    #                     else:
    #                         self.img_data[k]['continuous_legends'].add(field_type)
    #                 if field_name != 'None' and field_name != '':
    #                     self.img_data[k]['DATA'][field_name] = embedder[field_type][field_name]
    #                 else:
    #                     self.img_data[k]['DATA'][field_type] = embedder[field_type]
    #
    #
    # def create_imgs(self):
    #     print('Creating plots...')
    #     plots = {}
    #     for k, v in self.img_data.items():
    #         for categorical in v['categorical_legends']:
    #             fig, ax = plt.subplots()
    #             colmap = {name: n for n, name in enumerate(set(list(v['DATA'][categorical].unique())))}
    #             scatter = ax.scatter(v['DATA']['X'], v['DATA']['Y'], c=[colmap[name] for name in v['DATA'][categorical]], cmap=self.settings['CATEGORICAL_PALETTE'], s=self.settings['SCATTER_SIZE'])
    #             plt.legend(*scatter.legend_elements()).set_title(categorical)
    #             plt.xlabel('X')
    #             plt.ylabel('Y')
    #             plt_key = v['HASH'] + '_' + v['CLUSTERER_NAME'] + '_' + categorical
    #             title = 'EMBEDDER: {} \n CLUSTERER: {}'.format(v['HASH'], v['CLUSTERER_NAME'])
    #             if categorical != 'CLUSTER':
    #                 title = 'EMBEDDER: {}'.format(v['HASH'])
    #             plt.title(title, ha="center", fontsize=15, bbox={"facecolor": "orange", "alpha": 0.5, "pad": 0})
    #             plots[plt_key] = fig
    #             plt.close('all')
    #
    #         for continuous in v['continuous_legends']:
    #             fig, ax = plt.subplots()
    #             plt.xlabel('X')
    #             plt.ylabel('Y')
    #             points = ax.scatter(v['DATA']['X'], v['DATA']['Y'], c=v['DATA'][continuous], s=self.settings['SCATTER_SIZE'], cmap=self.settings['CONTINUOUS_PALETTE'])
    #             cbar = fig.colorbar(points)
    #             cbar.set_label(continuous, loc='center')
    #             title = 'EMBEDDER: {}'.format(v['HASH'])
    #             plt_key = v['HASH'] + v['CLUSTERER_NAME'] + '_' + continuous
    #             plt.title(title, ha="center", fontsize=15, bbox={"facecolor": "orange", "alpha": 0.5, "pad": 0})
    #             plots[plt_key] = fig
    #             plt.close('all')
    #
    #     for plt_key, fig in plots.items():
    #         save_path = os.path.join(self.save_dir, f'{plt_key}.png')
    #         print(f'Saving scatterplot {plt_key} ...')
    #         fig.savefig(save_path)
    #     self.timer.stop_timer()
    #     print(f'SIMBA COMPLETE: {str(len(plots.keys()))} plots saved in {self.save_dir} (elapsed time: {self.timer.elapsed_time_str}s)')


settings = {'palette': 'jet'}
test = GridSearchClusterVisualizer(model_dir='/Users/simon/Desktop/envs/troubleshooting/unsupervised/cluster_models',
                                   save_dir='/Users/simon/Desktop/envs/troubleshooting/unsupervised/images',
                                   settings=settings)
test.run()