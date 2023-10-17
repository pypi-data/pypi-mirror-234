import numpy as np
from simba.unsupervised.misc import check_directory_exists
import glob, os
import pandas as pd
from simba.misc_tools import check_if_filepath_list_is_empty
from simba.unsupervised.enums import Clustering, Unsupervised
from simba.mixins.unsupervised_mixin import UnsupervisedMixin
import seaborn as sns
import matplotlib.pyplot as plt
from simba.utils.printing import stdout_success


class GridSearchVisualizer(UnsupervisedMixin):
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

    def cluster_visualizer(self):
        data = self.read_pickle(self.model_dir)
        for k, v in data.items():
            self.check_key_exist_in_object(object=v, key=Clustering.CLUSTER_MODEL.value)
        for k, v in data.items():
            save_path = os.path.join(self.save_dir, f'{v[Unsupervised.DR_MODEL.value][Unsupervised.HASHED_NAME.value]}_{v[Clustering.CLUSTER_MODEL.value][Unsupervised.HASHED_NAME.value]}.png')
            data = pd.DataFrame(v[Unsupervised.DR_MODEL.value][Unsupervised.MODEL.value].embedding_, columns=['X', 'Y'])
            data['CLUSTER'] = v[Clustering.CLUSTER_MODEL.value][Unsupervised.MODEL.value].labels_.reshape(-1, 1).astype(np.int8)
            plot = sns.scatterplot(data=data, x='X', y='Y', hue="CLUSTER", palette=self.settings['PALETTE'])
            plt.savefig(save_path)
            stdout_success(msg=f'Saved {save_path}...')
            plt.close('all')
        self.timer.stop_timer()
        stdout_success(msg='All cluster images created.', elapsed_time=self.timer.elapsed_time_str)

    def categorical_visualizer(self,
                               categoricals: list):
        data = self.read_pickle(self.model_dir)
        for k, v in data.items():
            self.check_key_exist_in_object(object=v, key=Unsupervised.DR_MODEL.value)
        for k, v in data.items():
            for variable in categoricals:
                save_path = os.path.join(self.save_dir, f'{v[Unsupervised.DR_MODEL.value][Unsupervised.HASHED_NAME.value]}_{variable}.png')
                data = pd.DataFrame(v[Unsupervised.DR_MODEL.value][Unsupervised.MODEL.value].embedding_, columns=['X', 'Y'])
                data = pd.concat([v[Unsupervised.DATA.value][Unsupervised.BOUTS_FEATURES.value][variable], data], axis=1)
                plot = sns.scatterplot(data=data, x='X', y='Y', hue=variable, palette=self.settings['PALETTE'])
                plt.savefig(save_path)
                stdout_success(msg=f'Saved {save_path}...')
                plt.close('all')
        self.timer.stop_timer()
        stdout_success(msg='All cluster images created.', elapsed_time=self.timer.elapsed_time_str)

    def continuous_visualizer(self,
                             continuous_vars: list):
        data = self.read_pickle(self.model_dir)
        for k, v in data.items():
            self.check_key_exist_in_object(object=v, key=Unsupervised.DR_MODEL.value)
        for k, v in data.items():
            for variable in continuous_vars:
                save_path = os.path.join(self.save_dir, f'{v[Unsupervised.DR_MODEL.value][Unsupervised.HASHED_NAME.value]}_{variable}.png')
                fig, ax = plt.subplots()
                plt.xlabel('X')
                plt.ylabel('Y')
                data = pd.DataFrame(v[Unsupervised.DR_MODEL.value][Unsupervised.MODEL.value].embedding_, columns=['X', 'Y'])
                data = pd.concat([v[Unsupervised.DATA.value][Unsupervised.BOUTS_FEATURES.value][variable], data], axis=1)
                points = ax.scatter(data['X'], data['Y'], c=data[variable], s=self.settings['SCATTER_SIZE'], cmap=self.settings['PALETTE'])
                cbar = fig.colorbar(points)
                cbar.set_label(variable, loc='center')
                title = v[Unsupervised.DR_MODEL.value][Unsupervised.HASHED_NAME.value]
                plt.title(title, ha="center", fontsize=15, bbox={"facecolor": "orange", "alpha": 0.5, "pad": 0})
                fig.savefig(save_path)
                plt.close('all')
                stdout_success(msg=f'Saved {save_path}...')
        self.timer.stop_timer()
        stdout_success(msg='All cluster images created.', elapsed_time=self.timer.elapsed_time_str)



# settings = {'PALETTE': 'Pastel1'}
# test = GridSearchVisualizer(model_dir='/Users/simon/Desktop/envs/troubleshooting/unsupervised/cluster_models',
#                             save_dir='/Users/simon/Desktop/envs/troubleshooting/unsupervised/images',
#                             settings=settings)
# test.cluster_visualizer()


# settings = {'PALETTE': 'Pastel1', 'SCATTER_SIZE': 10}
# test = GridSearchVisualizer(model_dir='/Users/simon/Desktop/envs/troubleshooting/unsupervised/cluster_models',
#                             save_dir='/Users/simon/Desktop/envs/troubleshooting/unsupervised/images',
#                             settings=settings)
# test.continuous_visualizer(continuous_vars=['START_FRAME'])