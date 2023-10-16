__author__ = "Simon Nilsson", "JJ Choong"

import os, glob
from copy import deepcopy
import pandas as pd
from simba.rw_dfs import read_df, save_df
from simba.read_config_unit_tests import check_if_filepath_list_is_empty
from simba.utils.warnings import (ThirdPartyAnnotationsInvalidFileFormatWarning,
                                  ThirdPartyAnnotationsAdditionalClfWarning,
                                  ThirdPartyAnnotationsMissingAnnotationsWarning,
                                  ThirdPartyAnnotationEventCountWarning,
                                  ThirdPartyAnnotationOverlapWarning,
                                  ThirdPartyAnnotationsOutsidePoseEstimationDataWarning)
from simba.utils.errors import (InvalidFileTypeError,
                                ThirdPartyAnnotationsAdditionalClfError,
                                ThirdPartyAnnotationsMissingAnnotationsError,
                                ThirdPartyAnnotationEventCountError,
                                ThirdPartyAnnotationOverlapError,
                                ThirdPartyAnnotationsOutsidePoseEstimationDataError)
from simba.third_party_label_appenders.tools import check_stop_events_prior_to_start_events
from simba.feature_extractors.unit_tests import read_video_info
from simba.misc_tools import SimbaTimer, get_fn_ext, create_logger
from simba.mixins.config_reader import ConfigReader
from simba.enums import Methods


VIDEO_FILE = 'Video file'
HEADER_LINES = 'Number of header lines:'
RECORDING_TIME = 'Recording time'
BEHAVIOR = 'Behavior'
EVENT = 'Event'
STATE_START = 'state start'
STATE_STOP = 'state stop'
START = 'START'
STOP = 'STOP'

EXPECTED_FIELDS = [RECORDING_TIME, BEHAVIOR, EVENT]

class ImportEthovision(ConfigReader):
    """
    Class for appending ETHOVISION human annotations onto featurized pose-estimation data.
    Results are saved within the project_folder/csv/targets_inserted directory of
    the SimBA project (as parquets' or CSVs).

    Parameters
    ----------
    config_path: str
        path to SimBA project config file in Configparser format
    folder_path: str
        path to folder holding ETHOVISION data files is XLSX or XLS format

    Notes
    -----
    `Third-party import GitHub tutorial <https://github.com/sgoldenlab/simba/blob/master/docs/third_party_annot.md>`__.
    `Example of expected ETHOVISION file <https://github.com/sgoldenlab/simba/blob/master/misc/ethovision_example.xlsx>`__.

    Examples
    -----
    >>> ImportEthovision(config_path="MyConfigPath", folder_path="MyEthovisionFolderPath")
    """

    def __init__(self,
                 config_path: str,
                 data_dir: str,
                 settings: dict):

        super().__init__(config_path=config_path)
        print('Appending ETHOVISION annotations...')
        self.annot_file_paths = glob.glob(data_dir + '/*.xlsx') + glob.glob(data_dir + '/*.xls')
        self.annot_file_paths = [x for x in self.annot_file_paths if '~$' not in x]
        self.settings, self.error_settings = settings, settings['errors']
        if self.settings['log']: create_logger(path=os.path.join(self.logs_path, f'BORIS_append_{self.datetime}.log'))
        check_if_filepath_list_is_empty(filepaths=self.annot_file_paths,
                                        error_msg=f'SIMBA ERROR: No ETHOVISION xlsx or xls files found in {data_dir}.')
        check_if_filepath_list_is_empty(filepaths=self.feature_file_paths,
                                        error_msg='SIMBA ERROR: ZERO files found in the project_folder/csv/features_extracted directory')

    def __save(self):
        save_file_name = os.path.join(self.targets_folder, self.video_name + '.' + self.file_type)
        save_df(self.features_df, self.file_type, save_file_name)
        print('Added Ethovision annotations for video {} ... '.format(self.video_name))

    def run(self):
        self.data = {}
        for file_cnt, file_path in enumerate(self.annot_file_paths):
            _, video_name, _ = get_fn_ext(filepath=file_path)
            print(f'Reading ETHOVISION data file number {str(file_cnt+1)}...')
            try:
                df = pd.read_excel(file_path, sheet_name=None)
                sheet_name = list(df.keys())[-1]
                df = pd.read_excel(file_path, sheet_name=sheet_name, index_col=0, header=None)
                video_path = df.loc[VIDEO_FILE].values[0]
                _, video_name, ext = get_fn_ext(video_path)
                header_n = int(df.loc[HEADER_LINES].values[0]) - 2
                df = df.iloc[header_n:].reset_index(drop=True)
                df.columns = list(df.iloc[0])
                df = df.iloc[2:].reset_index(drop=True)[EXPECTED_FIELDS]
                self.data[video_name] = df
            except Exception as e:
                if self.error_settings[Methods.INVALID_THIRD_PARTY_APPENDER_FILE.value] == Methods.WARNING.value:
                    ThirdPartyAnnotationsInvalidFileFormatWarning(annotation_app='ETHOVISION', file_path=file_path, log_status=self.settings['log'])
                elif self.error_settings[Methods.INVALID_THIRD_PARTY_APPENDER_FILE.value] == Methods.ERROR.value:
                    raise InvalidFileTypeError(msg=f'{file_path} is not a valid ETHOVISION file. See the docs for expected file format.')
                else:
                    pass

        for file_path in self.feature_file_paths:
            _, self.video_name, _ = get_fn_ext(filepath=file_path)
            video_timer = SimbaTimer()
            video_timer.start_timer()
            x_df = read_df(file_path, self.file_type)
            out_df = deepcopy(x_df)
            annot_df = self.data[self.video_name]
            _, _, fps = read_video_info(vid_info_df=self.video_info_df, video_name=self.video_name)
            additional_clfs = list(set(annot_df[BEHAVIOR].unique()) - set(self.clf_names))
            if additional_clfs and self.error_settings[Methods.ADDITIONAL_THIRD_PARTY_CLFS.value] == Methods.WARNING.value:
                ThirdPartyAnnotationsAdditionalClfWarning(video_name=self.video_name, clf_names=additional_clfs)
            elif additional_clfs and self.error_settings[Methods.ADDITIONAL_THIRD_PARTY_CLFS.value] == Methods.ERROR.value:
                raise ThirdPartyAnnotationsAdditionalClfError(video_name=self.video_name, clf_names=additional_clfs)
            for clf in self.clf_names:
                clf_annot_df = annot_df[annot_df[BEHAVIOR] == clf]
                if (len(clf_annot_df) == 0) and self.error_settings[Methods.ZERO_THIRD_PARTY_VIDEO_ANNOTATIONS.value] == Methods.WARNING.value:
                    ThirdPartyAnnotationsMissingAnnotationsWarning(video_name=self.video_name, clf_names=[clf])
                    out_df[clf] = 0
                    continue
                elif (len(clf_annot_df) == 0) and self.error_settings[Methods.ZERO_THIRD_PARTY_VIDEO_ANNOTATIONS.value] == Methods.ERROR.value:
                    raise ThirdPartyAnnotationsMissingAnnotationsError(video_name=self.video_name, clf_names=[clf])
                clf_annot_start = pd.DataFrame(clf_annot_df[RECORDING_TIME][annot_df[EVENT] == STATE_START]).astype(float).sort_values(by=RECORDING_TIME)
                clf_annot_stop = pd.DataFrame(clf_annot_df[RECORDING_TIME][annot_df[EVENT] == STATE_STOP]).astype(float).sort_values(by=RECORDING_TIME)
                if (len(clf_annot_stop) != len(clf_annot_start)) and (self.error_settings[Methods.THIRD_PARTY_EVENT_COUNT_CONFLICT.value] == Methods.ERROR.value):
                    raise ThirdPartyAnnotationEventCountError(video_name=self.video_name, clf_name=clf, start_event_cnt=len(clf_annot_start), stop_event_cnt=len(clf_annot_stop))
                elif (len(clf_annot_stop) != len(clf_annot_start)) and (self.error_settings[Methods.THIRD_PARTY_EVENT_COUNT_CONFLICT.value] == Methods.WARNING.value):
                    ThirdPartyAnnotationEventCountWarning(video_name=self.video_name, clf_name=clf, start_event_cnt=len(clf_annot_start), stop_event_cnt=len(clf_annot_stop))
                    #TODO

                clf_starts = clf_annot_start[RECORDING_TIME].to_frame().rename(columns={RECORDING_TIME: START}).reset_index(drop=True)
                clf_stops = clf_annot_stop[RECORDING_TIME].to_frame().rename(columns={RECORDING_TIME: STOP}).reset_index(drop=True)
                clf_annot = pd.concat([clf_starts, clf_stops], axis=1).apply(pd.to_numeric)
                overlaps = check_stop_events_prior_to_start_events(df=clf_annot)
                if len(overlaps) > 0 and (self.error_settings[Methods.THIRD_PARTY_EVENT_OVERLAP.value] == Methods.ERROR.value):
                    raise ThirdPartyAnnotationOverlapError(video_name=self.video_name, clf_name=clf)
                if len(overlaps) > 0 and (self.error_settings[Methods.THIRD_PARTY_EVENT_OVERLAP.value] == Methods.WARNING.value):
                    ThirdPartyAnnotationOverlapWarning(video_name=self.video_name, clf_name=clf)
                    clf_annot = clf_annot.drop(index=list(overlaps.index)).reset_index(drop=True)
                clf_annot['START_FRAME'] = (clf_annot[START] * fps).astype(int)
                clf_annot['END_FRAME'] = (clf_annot[STOP] * fps).astype(int)
                annot_idx = list(clf_annot.apply(lambda x: list(range(int(x['START_FRAME']), int(x['END_FRAME']) + 1)), 1))
                annot_idx = [x for xs in annot_idx for x in xs]
                idx_diff = list(set(annot_idx) - set(out_df.index))
                if (len(idx_diff) > 0) and (self.error_settings[Methods.THIRD_PARTY_FRAME_COUNT_CONFLICT.value] == Methods.WARNING.value):
                    ThirdPartyAnnotationsOutsidePoseEstimationDataWarning(video_name=self.video_name,
                                                                          clf_name=clf,
                                                                          frm_cnt=out_df.index[-1],
                                                                          first_error_frm=idx_diff[0],
                                                                          ambiguous_cnt=len(idx_diff))
                elif (len(idx_diff) > 0) and (self.error_settings[Methods.THIRD_PARTY_FRAME_COUNT_CONFLICT.value] == Methods.ERROR.value):
                    raise ThirdPartyAnnotationsOutsidePoseEstimationDataError(video_name=self.video_name,
                                                                              clf_name=clf,
                                                                              frm_cnt=out_df.index[-1],
                                                                              first_error_frm=idx_diff[0],
                                                                              ambiguous_cnt=len(idx_diff))
                annot_idx = [x for x in annot_idx if x not in idx_diff]
                out_df[clf] = 0
                out_df.loc[annot_idx, clf] = 1
                self.__save()
                video_timer.stop_timer()
                print(f'Added Ethovision annotations for video {self.video_name} (elapsed time: {video_timer.elapsed_time_str}s)... ')

            self.timer.stop_timer()
            print(f'SIMBA COMPLETE: ETHOVISION annotations appended to dataset and saved in project_folder/csv/targets_inserted directory (elapsed time: {self.timer.elapsed_time_str}s).')


settings = {'log': False,
            'errors': {'INVALID annotations file data format': 'ERROR',
                       'ADDITIONAL third-party behavior detected': 'NONE',
                       'ZERO third-party video annotations found': 'WARNING',
                       'Annotations and pose FPS conflict': 'WARNING',
                       'Annotations EVENT COUNT inconsistency': 'ERROR',
                       'Annotations OVERLAP inaccuracy': 'WARNING',
                       'ZERO third-party video behavior annotations found': 'ERROR',
                       'Annotations and pose FRAME COUNT conflict': 'NONE',
                       'Annotations data file NOT FOUND': 'WARNING'}}


test = ImportEthovision(config_path= r"/Users/simon/Desktop/envs/simba_dev/tests/test_data/import_tests/project_folder/project_config.ini",
                        data_dir=r'/Users/simon/Desktop/envs/simba_dev/tests/test_data/import_tests/ethovision_data',
                        settings=settings)
test.run()
# test = ImportEthovision(config_path= r"/Users/simon/Desktop/simbapypi_dev/tests/test_data/multi_animal_dlc_two_c57/project_folder/project_config.ini", folder_path=r'/Users/simon/Desktop/simbapypi_dev/tests/test_data/multi_animal_dlc_two_c57/ethovision_import')
