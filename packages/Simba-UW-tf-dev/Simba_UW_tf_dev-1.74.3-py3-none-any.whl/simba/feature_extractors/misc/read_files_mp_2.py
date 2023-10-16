from typing import Optional, List
from typing_extensions import Literal
from simba.utils.read_write import get_fn_ext, read_df, find_core_cnt, get_memory_usage_of_df
from simba.utils.printing import SimbaTimer
from simba.utils.errors import ColumnNotFoundError, InvalidInputError, NoDataError
import pandas as pd
import platform
import concurrent
import glob

#@staticmethod
def _read_data_file_helper(file_path: str,
                           file_type: str,
                           clf_names: Optional[List[str]] = None):
    """
    Private function called by :meth:`simba.train_model_functions.read_all_files_in_folder_mp`
    """

    timer = SimbaTimer(start=True)
    _, vid_name, _ = get_fn_ext(file_path)
    df = read_df(file_path, file_type).dropna(axis=0, how='all').fillna(0)
    df.index = [vid_name] * len(df)
    if clf_names != None:
        for clf_name in clf_names:
            if not clf_name in df.columns:
                raise ColumnNotFoundError(column_name=clf_name, file_name=file_path)
            elif len(set(df[clf_name].unique()) - {0, 1}) > 0:
                raise InvalidInputError \
                    (msg=f'The annotation column for a classifier should contain only 0 or 1 values. However, in file {file_path} the {clf_name} field contains additional value(s): {list(set(df[clf_name].unique()) - {0, 1})}.', source=_read_data_file_helper.__name__)
    timer.stop_timer()
    print(f'Reading complete {vid_name} (elapsed time: {timer.elapsed_time_str}s)...')
    return df

#@staticmethod
def read_all_files_in_folder_mp(file_paths: List[str],
                                file_type: Literal['csv', 'parquet', 'pickle'],
                                classifier_names: Optional[List[str]] = None) -> pd.DataFrame:
    """

    Multiprocessing helper function to read in all data files in a folder to a single
    pd.DataFrame for downstream ML. Defaults to ceil(CPU COUNT / 2) cores. Asserts that all classifiers
    have annotation fields present in each dataframe.

    .. note::
      If multiprocess failure, reverts to :meth:`simba.mixins.train_model_mixin.read_all_files_in_folder`

    :parameter List[str] file_paths: List of file-paths
    :parameter List[str] file_paths: The filetype of ``file_paths`` OPTIONS: csv or parquet.
    :parameter Optional[List[str]] classifier_names: List of classifier names representing fields of human annotations. If not None, then assert that classifier names
        are present in each data file.
    :return pd.DataFrame: Concatenated dataframe of all data in ``file_paths``.

    """
    cpu_cnt, _ = find_core_cnt()
    df_lst = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_cnt) as executor:
        results = [executor.submit(_read_data_file_helper, data, file_type, classifier_names) for data in file_paths]
        for result in concurrent.futures.as_completed(results):
            df_lst.append(result.result())
    df_concat = pd.concat(df_lst, axis=0).round(4)
    if 'scorer' in df_concat.columns:
        df_concat = df_concat.drop(['scorer'], axis=1)
    memory_size = get_memory_usage_of_df(df=df_concat)
    print(f'Dataset size: {memory_size["megabytes"]}MB / {memory_size["gigabytes"]}GB')

        # with ProcessPoolExecutor(int(np.ceil(cpu_cnt / 2))) as pool:
        #     for res in pool.map(self._read_data_file_helper, file_paths, repeat(file_type), repeat(classifier_names)):
        #         df_lst.append(res)
        # df_concat = pd.concat(df_lst, axis=0).round(4)
        # if 'scorer' in df_concat.columns:
        #     df_concat = df_concat.drop(['scorer'], axis=1)
        # if len(df_concat) == 0:
        #     raise NoDataError \
        #         (msg='SimBA found 0 observations (frames) in the project_folder/csv/targets_inserted directory')
        # df_concat = df_concat.loc[:, ~df_concat.columns.str.contains('^Unnamed')].astype(np.float32)
        # memory_size = get_memory_usage_of_df(df=df_concat)
        # print(f'Dataset size: {memory_size["megabytes"]}MB / {memory_size["gigabytes"]}GB')
        # return df_concat


file_paths = glob.glob('/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/csv/targets_inserted' + '/*.csv')
read_all_files_in_folder_mp(file_paths=file_paths, file_type='csv', classifier_names=['Attack'])