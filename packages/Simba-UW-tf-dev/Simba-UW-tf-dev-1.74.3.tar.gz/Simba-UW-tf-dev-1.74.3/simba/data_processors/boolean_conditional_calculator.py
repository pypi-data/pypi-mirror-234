import pandas as pd

from simba.mixins.config_reader import ConfigReader
from typing import Dict, Union
import os
from simba.utils.checks import check_if_filepath_list_is_empty
from simba.utils.read_write import read_df, read_video_info, get_fn_ext, str_2_bool
from simba.utils.printing import stdout_success
from simba.utils.errors import MissingColumnsError, InvalidInputError
from simba.utils.warnings import NoDataFoundWarning
from simba.utils.data import detect_bouts
from copy import deepcopy
from simba.utils.enums import Options


class BooleanConditionalCalculator(ConfigReader):
    """
    Compute descriptive statistics (e.g., the time in seconds and number of frames) of multiple Boolean fields fullfilling user-defined conditions.

    For example, computedescriptive statistics for when Animal 1 is inside the shape Rectangle_1 while at the same time directing towards shape Polygon_1,
    while at the same time Animal 2 is outside shape Rectangle_1 and directing towards Polygon_1.

    :parameter str config_path: path to SimBA project config file in Configparser format.
    :parameter Dict[str, Union[bool, str]] rules: Rules with field names as keys and bools as values. Values can be strings (e.g., "TRUE", "FALSE") or bools (True, False).

    .. note:
       `Example expected output table <https://github.com/sgoldenlab/simba/blob/master/misc/Conditional_aggregate_statistics_20231004130314.csv>`__.

    Examples
    -----
    >>> rules = {'Rectangle_1 Simon in zone': 'TRUE', 'Polygon_1 JJ in zone': 'TRUE'}
    >>> conditional_bool_rule_calculator = BooleanConditionalCalculator(rules=rules, config_path='/Users/simon/Desktop/envs/troubleshooting/two_animals_16bp_032023/project_folder/project_config.ini')
    >>> conditional_bool_rule_calculator.run()
    >>> conditional_bool_rule_calculator.save()
    """

    def __init__(self,
                 config_path: str,
                 rules: Dict[str, Union[bool, str]]):

        ConfigReader.__init__(self, config_path=config_path)
        self.save_path = os.path.join(self.logs_path, f'Conditional_aggregate_statistics_{self.datetime}.csv')
        self.detailed_save_path = os.path.join(self.logs_path, f'Conditional_aggregate_detailed_{self.datetime}.csv')
        check_if_filepath_list_is_empty(filepaths=self.feature_file_paths, error_msg=f'No data found in {self.features_dir}')
        self.rules = rules
        self.output_df = pd.DataFrame(columns=['VIDEO'] + list(self.rules.keys()) + ['TIME (s)', 'FRAMES (count)'])
        self._check_rules_val_dtype()

    def _check_rules_val_dtype(self):
        for rule_behavior, rule_val in self.rules.items():
            if isinstance(rule_val, str):
                if rule_val.lower() == Options.BOOL_STR_OPTIONS.value[0].lower():
                    self.rules[rule_behavior] = True
                elif rule_val.lower() == Options.BOOL_STR_OPTIONS.value[1].lower():
                    self.rules[rule_behavior] = False
                else:
                    raise InvalidInputError(msg=f'Invalid input for behavior {rule_behavior}: {rule_val}', source=self.__class__.__name__)
            elif isinstance(rule_val, bool):
                pass
            else:
                raise InvalidInputError(msg=f'Invalid datatype for behavior {rule_behavior}: {rule_val}', source=self.__class__.__name__)
        self.values = list(self.rules.values())

    def _check_integrity_of_rule_columns(self):
        for behavior in self.rules.keys():
            if behavior not in self.df.columns:
                raise MissingColumnsError(msg=f'File is missing the column {behavior} which is required for your conditional aggregate statistics {self.file_path}', source=self.__class__.__name__)
            other_col_vals = [x for x in list(set(self.df[behavior])) if x not in [0, 1]]
            if len(other_col_vals) > 0:
                raise InvalidInputError(msg=f'Invalid values found in column {behavior} of file {self.file_path}: SimBA expects only 0 and 1s.', source=self.__class__.__name__)

    def run(self):
        self.bout_lst = []
        for file_cnt, file_path in enumerate(self.feature_file_paths):
            self.file_path = file_path
            _, self.video_name, _ = get_fn_ext(filepath=file_path)
            print(f'Analyzing {self.video_name} (video {file_cnt+1}/{len(self.feature_file_paths)})...')
            _, _, self.fps = read_video_info(vid_info_df=self.video_info_df, video_name=self.video_name)
            self.df = read_df(file_path=file_path, file_type=self.file_type)
            self._check_integrity_of_rule_columns()
            self.df = self.df[list(self.rules.keys())]
            self.sliced_df = deepcopy(self.df)
            values_str = []
            for k, v in self.rules.items():
                if v:
                    self.sliced_df = self.sliced_df[self.sliced_df[k] == 1]
                else:
                    self.sliced_df = self.sliced_df[self.sliced_df[k] == 0]
                values_str.append(v)
            time_s = round(len(self.sliced_df) / self.fps, 4)
            self.output_df.loc[len(self.output_df)] = [self.video_name] + list(self.rules.values()) + [time_s] + [len(self.sliced_df)]
            self.df['BEHAVIOR'] = 0; self.df.loc[self.sliced_df.index, 'BEHAVIOR'] = 1
            bouts = detect_bouts(data_df=self.df, target_lst=['BEHAVIOR'], fps=1)[['Start_frame', 'End_frame']]
            bouts['VIDEO'] = self.video_name
            bout_output_cols = ['VIDEO']
            for i in range(len(list(self.rules.keys()))):
                bouts[list(self.rules.keys())[i]] = list(self.rules.values())[i]
                bout_output_cols.append(list(self.rules.keys())[i])
            bout_output_cols.extend(('Start_frame', 'End_frame'))
            self.bout_lst.append(bouts[bout_output_cols])

    def save(self):
        bout_df = pd.concat(self.bout_lst, axis=0)
        if len(bout_df) == 0:
            NoDataFoundWarning(msg='No frames in any video found fulfilling user criterion.')
        bout_df.to_csv(self.detailed_save_path, index=False)
        self.output_df.to_csv(self.save_path, index=False)
        self.timer.stop_timer()
        stdout_success(msg=f'Boolean conditional AGGREGATE data saved at at {self.save_path}!', elapsed_time=self.timer.elapsed_time_str, source=self.__class__.__name__)
        stdout_success(msg=f'Boolean conditional DETAILED data saved at at {self.detailed_save_path}!', elapsed_time=self.timer.elapsed_time_str, source=self.__class__.__name__)

# rules = {'Rectangle_1 Simon in zone': True, 'Polygon_1 JJ in zone': True}
# runner = BooleanConditionalCalculator(rules=rules, config_path='/Users/simon/Desktop/envs/troubleshooting/two_animals_16bp_032023/project_folder/project_config.ini')
# runner.run()
# runner.save()