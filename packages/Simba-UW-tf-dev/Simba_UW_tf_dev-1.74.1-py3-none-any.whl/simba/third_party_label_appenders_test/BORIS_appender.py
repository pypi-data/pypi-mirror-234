__author__ = "Simon Nilsson"

from simba.read_config_unit_tests import (check_if_dir_exists,
                                          check_if_filepath_list_is_empty)
from simba.mixins.config_reader import ConfigReader
import os, glob
from simba.rw_dfs import read_df, save_df
from simba.misc_tools import get_fn_ext, create_logger
from simba.third_party_label_appenders.tools import check_stop_events_prior_to_start_events, fix_uneven_start_stop_count
from simba.feature_extractors.unit_tests import read_video_info
from simba.utils.errors import (ThirdPartyAnnotationOverlapError,
                                ThirdPartyAnnotationEventCountError,
                                InvalidFileTypeError,
                                ThirdPartyAnnotationsMissingAnnotationsError,
                                ThirdPartyAnnotationsFpsConflictError,
                                ThirdPartyAnnotationsClfMissingError,
                                ThirdPartyAnnotationsOutsidePoseEstimationDataError,
                                ThirdPartyAnnotationsAdditionalClfError)
from simba.utils.warnings import (ThirdPartyAnnotationsOutsidePoseEstimationDataWarning,
                                  ThirdPartyAnnotationsInvalidFileFormatWarning,
                                  ThirdPartyAnnotationsAdditionalClfWarning,
                                  ThirdPartyAnnotationsMissingAnnotationsWarning,
                                  ThirdPartyAnnotationsFpsConflictWarning,
                                  ThirdPartyAnnotationEventCountWarning,
                                  ThirdPartyAnnotationOverlapWarning,
                                  ThirdPartyAnnotationsClfMissingWarning)
import pandas as pd
from simba.enums import Methods
from copy import deepcopy

MEDIA_FILE_PATH = 'Media file path'
OBSERVATION_ID = 'Observation id'
TIME = 'Time'
FPS = 'FPS'
BEHAVIOR = 'Behavior'
STATUS = 'Status'
START = 'START'
STOP = 'STOP'
DATA_FILE_TYPE = 'csv'

EXPECTED_HEADERS = [TIME, MEDIA_FILE_PATH, FPS, BEHAVIOR, STATUS]

class BorisAppender(ConfigReader):

    """
    Class for appending BORIS human annotations onto featurized pose-estimation data.

    Parameters
    ----------
    config_path: str
        path to SimBA project config file in Configparser format
    boris_folder: str
        path to folder holding BORIS data files is CSV format

    Notes
    ----------
    `Example BORIS input file <https://github.com/sgoldenlab/simba/blob/master/misc/boris_example.csv`__.

    Examples
    ----------
    >>> boris_appender = BorisAppender(config_path='MyProjectConfigPath', data_dir=r'BorisDataFolder')
    >>> boris_appender.create_boris_master_file()
    >>> boris_appender.run()

    References
    ----------

    .. [1] `Behavioral Observation Research Interactive Software (BORIS) user guide <https://boris.readthedocs.io/en/latest/#>`__.
    """

    def __init__(self,
                 config_path: str,
                 data_dir: str,
                 settings: dict):

        super().__init__(config_path=config_path)
        check_if_dir_exists(in_dir=data_dir)
        self.data_dir, self.settings = data_dir, settings
        self.error_settings = self.settings['errors']
        if self.settings['log']:
            create_logger(path=os.path.join(self.logs_path, f'BORIS_append_{self.datetime}.log'))
        self.data_file_paths = glob.glob(self.data_dir + f'/*.{DATA_FILE_TYPE}')
        check_if_filepath_list_is_empty(filepaths=self.data_file_paths,
                                        error_msg=f'SIMBA ERROR: ZERO BORIS CSV files found in {data_dir} directory')
        check_if_filepath_list_is_empty(filepaths=self.feature_file_paths,
                                        error_msg='SIMBA ERROR: ZERO files found in the project_folder/csv/features_extracted directory')
        print(f'Processing BORIS for {str(len(self.feature_file_paths))} file(s)...')

    def __read(self):
        self.df_lst = []
        for file_cnt, file_path in enumerate(self.data_file_paths):
            _, video_name, _ = get_fn_ext(file_path)
            boris_df = pd.read_csv(file_path)
            try:
                start_idx = (boris_df[boris_df[OBSERVATION_ID] == TIME].index.values)
                df = pd.read_csv(file_path, skiprows=range(0, int(start_idx + 1)))[EXPECTED_HEADERS]
                _, video_base_name, _ = get_fn_ext(df.loc[0, MEDIA_FILE_PATH])
                df[MEDIA_FILE_PATH] = video_base_name
                self.df_lst.append(df)
            except Exception as e:
                if self.error_settings[Methods.INVALID_THIRD_PARTY_APPENDER_FILE.value] == Methods.WARNING.value:
                    ThirdPartyAnnotationsInvalidFileFormatWarning(annotation_app='BORIS', file_path=file_path, log_status=self.settings['log'])
                elif self.error_settings[Methods.INVALID_THIRD_PARTY_APPENDER_FILE.value] == Methods.ERROR.value:
                    raise InvalidFileTypeError(msg=f'{file_path} is not a valid BORIS file. See the docs for expected file format.')
                else:
                    pass
        self.df = pd.concat(self.df_lst, axis=0).reset_index(drop=True)
        del self.df_lst

    def __save(self):
        save_path = os.path.join(self.targets_folder, self.video_name + '.' + self.file_type)
        save_df(self.out_df, self.file_type, save_path)
        print('Saved BORIS annotations for video {}...'.format(self.video_name))

    def __append(self):
        for file_cnt, file_path in enumerate(self.feature_file_paths):
            _, self.video_name, _ = get_fn_ext(file_path)
            _, _, fps = read_video_info(vid_info_df=self.video_info_df, video_name=self.video_name)
            print('Appending BORIS annotations to {} ...'.format(self.video_name))
            data_df = read_df(file_path, self.file_type)
            self.out_df = deepcopy(data_df)
            video_annot = self.df.loc[self.df[MEDIA_FILE_PATH] == self.video_name]
            video_annot = video_annot.loc[(video_annot[STATUS] == START) | (video_annot[STATUS] == STOP)]
            additional_clfs = list(set(self.df[BEHAVIOR].unique()) - set(self.clf_names))
            if additional_clfs and self.error_settings[Methods.ADDITIONAL_THIRD_PARTY_CLFS.value] == Methods.WARNING.value:
                ThirdPartyAnnotationsAdditionalClfWarning(video_name=self.video_name, clf_names=additional_clfs)
            elif additional_clfs and self.error_settings[Methods.ADDITIONAL_THIRD_PARTY_CLFS.value] == Methods.ERROR.value:
                raise ThirdPartyAnnotationsAdditionalClfError(video_name=self.video_name, clf_names=additional_clfs)
            video_annot = video_annot[video_annot[BEHAVIOR].isin(self.clf_names)]
            if (len(video_annot) == 0) and self.error_settings[Methods.ZERO_THIRD_PARTY_VIDEO_ANNOTATIONS.value] == Methods.WARNING.value:
                ThirdPartyAnnotationsMissingAnnotationsWarning(video_name=self.video_name, clf_names=self.clf_names)
                for clf in self.clf_names: self.out_df[clf] = 0
                continue
            elif (len(video_annot) == 0) and self.error_settings[Methods.ZERO_THIRD_PARTY_VIDEO_ANNOTATIONS.value] == Methods.ERROR.value:
                raise ThirdPartyAnnotationsMissingAnnotationsError(video_name=self.video_name, clf_names=self.clf_names)
            boris_fps = round(video_annot[FPS].values[0])
            if (int(boris_fps) != int(fps)) and (self.error_settings[Methods.THIRD_PARTY_FPS_CONFLICT.value] == Methods.WARNING.value):
                ThirdPartyAnnotationsFpsConflictWarning(video_name=self.video_name, annotation_fps=int(boris_fps), video_fps=int(fps))
            if (int(boris_fps) != int(fps)) and (self.error_settings[Methods.THIRD_PARTY_FPS_CONFLICT.value] == Methods.ERROR.value):
                raise ThirdPartyAnnotationsFpsConflictError(video_name=self.video_name, annotation_fps=int(boris_fps), video_fps=int(fps))

            for clf in self.clf_names:
                clf_annot = video_annot[(video_annot[BEHAVIOR] == clf)].reset_index(drop=True)
                clf_annot[TIME] = clf_annot[TIME].astype(float)
                clf_annot = clf_annot.sort_values(by=TIME)
                clf_annot_start = clf_annot[clf_annot[STATUS] == START].reset_index(drop=True)
                clf_annot_stop = clf_annot[clf_annot[STATUS] == STOP].reset_index(drop=True)
                if (len(clf_annot_stop) != len(clf_annot_start)) and (self.error_settings[Methods.THIRD_PARTY_EVENT_COUNT_CONFLICT.value] == Methods.ERROR.value):
                    raise ThirdPartyAnnotationEventCountError(video_name=self.video_name, clf_name=clf, start_event_cnt=len(clf_annot_start), stop_event_cnt=len(clf_annot_stop))
                elif (len(clf_annot_stop) != len(clf_annot_start)) and (self.error_settings[Methods.THIRD_PARTY_EVENT_COUNT_CONFLICT.value] == Methods.WARNING.value):
                    ThirdPartyAnnotationEventCountWarning(video_name=self.video_name, clf_name=clf, start_event_cnt=len(clf_annot_start), stop_event_cnt=len(clf_annot_stop), log_status=self.settings['log'])
                    results = fix_uneven_start_stop_count(starts=clf_annot_start[TIME].values, stops=clf_annot_stop[TIME].values)
                    clf_annot_start = results['START TIME'].to_frame().rename(columns={'START TIME': TIME})
                    clf_annot_stop = results['END TIME'].to_frame().rename(columns={'END TIME': TIME})
                self.clf_starts = clf_annot_start[TIME].to_frame().rename(columns={TIME: START}).reset_index(drop=True)
                self.clf_stops = clf_annot_stop[TIME].to_frame().rename(columns={TIME: STOP}).reset_index(drop=True)
                clf_annot = pd.concat([self.clf_starts, self.clf_stops], axis=1).apply(pd.to_numeric)
                overlaps, overlaps_idx = check_stop_events_prior_to_start_events(df=clf_annot)
                if len(overlaps) > 0 and (self.error_settings[Methods.THIRD_PARTY_EVENT_OVERLAP.value] == Methods.ERROR.value):
                    raise ThirdPartyAnnotationOverlapError(video_name=self.video_name, clf_name=clf, overlaps=overlaps)
                if len(overlaps) > 0 and (self.error_settings[Methods.THIRD_PARTY_EVENT_OVERLAP.value] == Methods.WARNING.value):
                    ThirdPartyAnnotationOverlapWarning(video_name=self.video_name, clf_name=clf, overlaps=overlaps, log_status=self.settings['log'])
                    clf_annot = clf_annot.drop(index=overlaps_idx).reset_index(drop=True)
                clf_annot['START_FRAME'] = (clf_annot[START] * fps).astype(int)
                clf_annot['END_FRAME'] = (clf_annot[STOP] * fps).astype(int)
                if (len(clf_annot) == 0) and (self.error_settings[Methods.ZERO_THIRD_PARTY_VIDEO_BEHAVIOR_ANNOTATIONS.value] == Methods.WARNING.value):
                    ThirdPartyAnnotationsClfMissingWarning(video_name=self.video_name, clf_name=clf)
                    self.out_df[clf] = 0
                    continue
                elif (len(clf_annot) == 0) and (self.error_settings[Methods.ZERO_THIRD_PARTY_VIDEO_BEHAVIOR_ANNOTATIONS.value] == Methods.ERROR.value):
                    raise ThirdPartyAnnotationsClfMissingError(video_name=self.video_name, clf_name=clf)
                annot_idx = list(clf_annot.apply(lambda x: list(range(int(x['START_FRAME']), int(x['END_FRAME']) + 1)), 1))
                annot_idx = [x for xs in annot_idx for x in xs]
                idx_diff = list(set(annot_idx) - set(self.out_df.index))
                if (len(idx_diff) > 0) and (self.error_settings[Methods.THIRD_PARTY_FRAME_COUNT_CONFLICT.value] == Methods.WARNING.value):
                    ThirdPartyAnnotationsOutsidePoseEstimationDataWarning(video_name=self.video_name,
                                                                          clf_name=clf,
                                                                          frm_cnt=self.out_df.index[-1],
                                                                          first_error_frm=idx_diff[0],
                                                                          ambiguous_cnt=len(idx_diff))
                elif (len(idx_diff) > 0) and (self.error_settings[Methods.THIRD_PARTY_FRAME_COUNT_CONFLICT.value] == Methods.ERROR.value):
                    raise ThirdPartyAnnotationsOutsidePoseEstimationDataError(video_name=self.video_name,
                                                                          clf_name=clf,
                                                                          frm_cnt=self.out_df.index[-1],
                                                                          first_error_frm=idx_diff[0],
                                                                          ambiguous_cnt=len(idx_diff))
                annot_idx = [x for x in annot_idx if x not in idx_diff]
                self.out_df[clf] = 0
                self.out_df.loc[annot_idx, clf] = 1
            self.__save()

    def run(self):
        self.__read()
        self.__append()
        self.timer.stop_timer()
        print(f'SIMBA COMPLETE: BORIS annotations appended to dataset and saved in project_folder/csv/targets_inserted directory (elapsed time: {self.timer.elapsed_time_str}s).')

settings = {'log': True, 'errors': {'INVALID annotations file data format': 'NONE',
                                     'ADDITIONAL third-party behavior detected': 'NONE',
                                     'ZERO third-party video annotations found': 'NONE',
                                     'Annotations and pose FPS conflict': 'WARNING',
                                     'Annotations EVENT COUNT inconsistency': 'WARNING',
                                     'Annotations OVERLAP inaccuracy': 'WARNING',
                                     'ZERO third-party video behavior annotations found': 'WARNING',
                                     'Annotations and pose FRAME COUNT conflict': 'WARNING',
                                     'Annotations data file NOT FOUND': 'NONE'}}

test = BorisAppender(config_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini',
                     data_dir='/Users/simon/Downloads/FIXED', settings=settings)
test.run()

# test = BorisAppender(config_path='/Users/simon/Desktop/troubleshooting/train_model_project/project_folder/project_config.ini', boris_folder=r'/Users/simon/Desktop/troubleshooting/train_model_project/boris_import')
# test.create_boris_master_file()
# test.append_boris()

# test = BorisAppender(config_path='/Users/simon/Desktop/envs/marcel_boris/project_folder/project_config.ini', boris_folder=r'/Users/simon/Desktop/envs/marcel_boris/BORIS_data')
# test.create_boris_master_file()
# test.append_boris()

# test = BorisAppender(config_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini',
#                      boris_folder='/Users/simon/Downloads/FIXED')
# test.create_boris_master_file()
# test.append_boris()
