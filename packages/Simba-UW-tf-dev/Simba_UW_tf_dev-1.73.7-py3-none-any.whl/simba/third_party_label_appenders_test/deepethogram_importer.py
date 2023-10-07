__author__ = "Simon Nilsson"

from simba.rw_dfs import read_df, save_df
import os, glob
from copy import deepcopy
import pandas as pd
from simba.utils.warnings import (ThirdPartyAnnotationsAdditionalClfWarning,
                                  ThirdPartyAnnotationsClfMissingWarning,
                                  ThirdPartyAnnotationsOutsidePoseEstimationDataWarning)
from simba.utils.errors import (ThirdPartyAnnotationsAdditionalClfError,
                                ThirdPartyAnnotationsClfMissingError,
                                ThirdPartyAnnotationsOutsidePoseEstimationDataError)
from simba.third_party_label_appenders.tools import match_feature_file_names_to_annotation_file_names
from simba.misc_tools import get_fn_ext, create_logger, SimbaTimer
from simba.enums import Methods
from simba.read_config_unit_tests import (check_if_filepath_list_is_empty,
                                          check_if_dir_exists)
from simba.mixins.config_reader import ConfigReader

BACKGROUND = 'background'

class DeepEthogramImporter(ConfigReader):

    """
    Class for appending DeepEthogram optical flow annotations onto featurized pose-estimation data.

    Parameters
    ----------
    config_path: str
        path to SimBA project config file in Configparser format
    deep_ethogram_dir: str
        path to folder holding DeepEthogram data files is CSV format

    Notes
    ----------
    `Third-party import tutorials <https://github.com/sgoldenlab/simba/blob/master/docs/third_party_annot.md>`__.
    `Example expected input <https://github.com/sgoldenlab/simba/blob/master/misc/deep_ethogram_labels.csv>`__.

    Examples
    ----------
    >>> deepethogram_importer = DeepEthogramImporter(config_path=r'MySimBAConfigPath', deep_ethogram_dir=r'MyDeepEthogramDir')
    >>> deepethogram_importer.import_deepethogram()

    References
    ----------

    .. [1] `DeepEthogram repo <https://github.com/jbohnslav/deepethogram>`__.
    .. [2] `Example DeepEthogram input file <https://github.com/sgoldenlab/simba/blob/master/misc/deep_ethogram_labels.csv>`__.
    """

    def __init__(self,
                 data_dir: str,
                 config_path: str,
                 settings: dict):

        super().__init__(config_path=config_path)
        self.data_dir = data_dir
        self.settings, self.error_settings = settings, settings['errors']
        if self.settings['log']: create_logger(path=os.path.join(self.logs_path, f'BORIS_append_{self.datetime}.log'))
        check_if_dir_exists(in_dir=self.data_dir)
        self.deepethogram_files_found = glob.glob(self.data_dir + '/*.csv')
        check_if_filepath_list_is_empty(filepaths=self.deepethogram_files_found,
                                        error_msg=f'SIMBA ERROR: ZERO DeepEthogram CSV files found in {self.data_dir} directory')
        check_if_filepath_list_is_empty(filepaths=self.feature_file_paths,
                                        error_msg='SIMBA ERROR: ZERO files found in the project_folder/csv/features_extracted directory')

    def import_deepethogram(self):
        matches = match_feature_file_names_to_annotation_file_names(annotation_file_paths=self.deepethogram_files_found,
                                                          feature_file_paths=self.feature_file_paths,
                                                          log_status=self.settings['log'],
                                                          setting=self.settings['errors'][Methods.THIRD_PARTY_ANNOTATION_FILE_NOT_FOUND.value])
        for cnt, (k, v) in enumerate(matches.items()):
            _, video_name, _ = get_fn_ext(filepath=v)
            video_timer = SimbaTimer()
            video_timer.start_timer()
            annot_df = read_df(file_path=k, file_type=self.file_type).reset_index(drop=True)
            annot_clfs = [x for x in annot_df.columns if x != BACKGROUND]
            x_df = read_df(file_path=v, file_type=self.file_type).reset_index(drop=True)
            out_df = deepcopy(x_df)
            additional_clfs = list(set(annot_clfs) - set(self.clf_names))
            if additional_clfs and self.error_settings[Methods.ADDITIONAL_THIRD_PARTY_CLFS.value] == Methods.WARNING.value:
                ThirdPartyAnnotationsAdditionalClfWarning(video_name=video_name, clf_names=additional_clfs, log_status=self.settings['log'])
            elif additional_clfs and self.error_settings[Methods.ADDITIONAL_THIRD_PARTY_CLFS.value] == Methods.ERROR.value:
                raise ThirdPartyAnnotationsAdditionalClfError(video_name=video_name, clf_names=additional_clfs)
            for clf in self.clf_names:
                if ((clf not in annot_clfs) and self.error_settings[Methods.ZERO_THIRD_PARTY_VIDEO_BEHAVIOR_ANNOTATIONS.value] == Methods.WARNING.value) :
                    ThirdPartyAnnotationsClfMissingWarning(video_name=video_name, clf_name=clf)
                    out_df[clf] = 0
                    continue
                elif ((clf not in annot_clfs) and self.error_settings[Methods.ZERO_THIRD_PARTY_VIDEO_BEHAVIOR_ANNOTATIONS.value] == Methods.ERROR.value) :
                    raise ThirdPartyAnnotationsClfMissingError(video_name=video_name, clf_name=clf)
                if (len(annot_df) != len(x_df)) and (self.error_settings[Methods.THIRD_PARTY_FRAME_COUNT_CONFLICT.value] == Methods.WARNING.value):
                    ThirdPartyAnnotationsOutsidePoseEstimationDataWarning(video_name=video_name,
                                                                          frm_cnt=len(x_df),
                                                                          annotation_frms=len(annot_df),
                                                                          log_status=self.settings['log'])
                    if len(annot_df) > len(x_df):
                        annot_df = annot_df.head(len(x_df))
                    if len(annot_df) < len(x_df):
                        padding = pd.DataFrame([[0] * (len(x_df) - len(annot_df))], columns=annot_df)
                        annot_df = annot_df.append(padding, ignore_index=True).reset_index(drop=True)

                if (len(annot_df) != len(x_df)) and (self.error_settings[Methods.THIRD_PARTY_FRAME_COUNT_CONFLICT.value] == Methods.ERROR.value):
                    raise ThirdPartyAnnotationsOutsidePoseEstimationDataError(video_name=video_name,
                                                                              frm_cnt=len(x_df),
                                                                              annotation_frms=len(annot_df))
                out_df[clf] = annot_df[clf]
                if (out_df[clf].sum() == 0) and (self.error_settings[Methods.ZERO_THIRD_PARTY_VIDEO_BEHAVIOR_ANNOTATIONS.value] == Methods.WARNING.value):
                    ThirdPartyAnnotationsClfMissingWarning(video_name=video_name, clf_name=clf)
                elif (out_df[clf].sum() == 0) and (self.error_settings[Methods.ZERO_THIRD_PARTY_VIDEO_BEHAVIOR_ANNOTATIONS.value] == Methods.ERROR.value) :
                    raise ThirdPartyAnnotationsClfMissingError(video_name=video_name, clf_name=clf)

            save_path = os.path.join(self.targets_folder, video_name + '.' + self.file_type)
            save_df(df=out_df, file_type=self.file_type, save_path=save_path)
            video_timer.stop_timer()
            print(f'DeepEthogram annotation for video {video_name} saved (elapsed time: {video_timer.elapsed_time_str}s)...')

        self.timer.stop_timer()
        print(f'SIMBA COMPLETE: DeepEthogram saved to files in the project_folder/csv/targets_inserted directory (elapsed time {self.timer.elapsed_time_str}s.')

settings = {'log': False,
            'errors': {'INVALID annotations file data format': 'NONE',
                       'ADDITIONAL third-party behavior detected': 'ERROR',
                       'ZERO third-party video annotations found': 'NONE',
                       'Annotations and pose FPS conflict': 'WARNING',
                       'Annotations EVENT COUNT inconsistency': 'WARNING',
                       'Annotations OVERLAP inaccuracy': 'WARNING',
                       'ZERO third-party video behavior annotations found': 'ERROR',
                       'Annotations and pose FRAME COUNT conflict': 'ERROR',
                       'Annotations data file NOT FOUND': 'WARNING'}}


test = DeepEthogramImporter(data_dir='/Users/simon/Desktop/envs/simba_dev/tests/test_data/deepethogram_example',
                            config_path='/Users/simon/Desktop/envs/simba_dev/tests/test_data/import_tests/project_folder/project_config.ini',
                            settings=settings)
test.import_deepethogram()