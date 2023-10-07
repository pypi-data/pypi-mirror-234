import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from simba.utils.read_write import read_df
from typing import List, Optional
from simba.utils.read_write import find_core_cnt
from simba.mixins.config_reader import ConfigReader
from simba.utils.printing import SimbaTimer, stdout_success
from itertools import repeat
import os
import shap
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from simba.utils.warnings import NotEnoughDataWarning
from simba.plotting.shap_agg_stats_visualizer import ShapAggregateStatisticsVisualizer




def _create_shap_mp_helper(data: pd.DataFrame,
                    clf_name: str,
                    explainer: shap.TreeExplainer,
                    clf: RandomForestClassifier,
                    expected_value: float):

    target = data.pop(clf_name).values.reshape(-1, 1)
    frame_batch_shap = explainer.shap_values(data.values, check_additivity=False)[1]
    shap_sum = np.sum(frame_batch_shap, axis=1).reshape(-1, 1)
    proba = clf.predict_proba(data)[:, 1].reshape(-1, 1)
    frame_batch_shap = np.hstack((frame_batch_shap, np.full((frame_batch_shap.shape[0]), expected_value).reshape(-1, 1), shap_sum, proba, target))
    return frame_batch_shap, data.values[0]

def create_shap_log_mp(ini_file_path: str,
                       rf_clf: RandomForestClassifier,
                       x_df: pd.DataFrame,
                       y_df: pd.DataFrame,
                       x_names: List[str],
                       clf_name: str,
                       cnt_present: int,
                       cnt_absent: int,
                       save_path: str,
                       batch_size: int = 10,
                       save_it: int = 100,
                       save_file_no: Optional[int] = None) -> None:
    """
    Helper to compute SHAP values using multiprocessing.
    For single-core alternative, see  meth:`simba.mixins.train_model_mixins.TrainModelMixin.create_shap_log_mp`.

    .. seealso::
       `Documentation <https://github.com/sgoldenlab/simba/blob/master/docs/Scenario1.md#train-predictive-classifiers-settings>`_

       .. image:: _static/img/shap.png
          :width: 400
          :align: center

    :param str ini_file_path: Path to the SimBA project_config.ini
    :param RandomForestClassifier rf_clf: sklearn random forest classifier
    :param pd.DataFrame x_df: Test features.
    :param pd.DataFrame y_df: Test target.
    :param List[str] x_names: Feature names.
    :param str clf_name: Classifier name.
    :param int cnt_present: Number of behavior-present frames to calculate SHAP values for.
    :param int cnt_absent: Number of behavior-absent frames to calculate SHAP values for.
    :param str save_dir: Directory where to save output in csv file format.
    :param Optional[int] save_file_no: If integer, represents the count of the classifier within a grid search. If none, the classifier is not
        part of a grid search.

    """

    print('Calculating SHAP values...')
    shap_timer = SimbaTimer(start=True)
    data_df = pd.concat([x_df, y_df], axis=1)
    if save_file_no == None:
        out_df_shap_path = os.path.join(save_path, f'SHAP_values_{clf_name}.csv')
        out_df_raw_path = os.path.join(save_path, f'RAW_SHAP_feature_values_{clf_name}.csv')
    else:
        out_df_shap_path = os.path.join(save_path, f'SHAP_values_{str(save_file_no)}_{clf_name}.csv')
        out_df_raw_path = os.path.join(save_path, f'RAW_SHAP_feature_values_{str(save_file_no)}_{clf_name}.csv')
    target_df, nontarget_df = data_df[data_df[y_df.name] == 1], data_df[data_df[y_df.name] == 0]
    if len(target_df) < cnt_present:
        NotEnoughDataWarning(msg=f'Train data contains {str(len(target_df))} behavior-present annotations. This is less the number of frames you specified to calculate shap values for {str(cnt_present)}. SimBA will calculate shap scores for the {str(len(target_df))} behavior-present frames available')
        cnt_present = len(target_df)
    if len(nontarget_df) < cnt_absent:
        NotEnoughDataWarning(msg=f'Train data contains {str(len(nontarget_df))} behavior-absent annotations. This is less the number of frames you specified to calculate shap values for {str(cnt_absent)}. SimBA will calculate shap scores for the {str(len(target_df))} behavior-absent frames available')
        cnt_absent = len(nontarget_df)
    non_target_for_shap = nontarget_df.sample(cnt_absent, replace=False)
    targets_for_shap = target_df.sample(cnt_present, replace=False)
    explainer = shap.TreeExplainer(rf_clf, data=None, model_output='raw', feature_perturbation='tree_path_dependent')
    expected_value = explainer.expected_value[1]
    cores, _ = find_core_cnt()
    shap_data_df = pd.concat([targets_for_shap, non_target_for_shap], axis=0)
    if (len(shap_data_df) / batch_size) < 1:
        batch_size = 1
    elif (len(shap_data_df) > 100) & (save_it >= 100):
        batch_size = 100
    shap_data = np.array_split(shap_data_df, len(shap_data_df) / batch_size)
    shap_results, shap_raw, processed_counter = [], [], 0
    with ProcessPoolExecutor(int(np.ceil(cores / 2))) as pool:
        for it_cnt, res in enumerate(pool.map(_create_shap_mp_helper, shap_data, repeat(clf_name), repeat(explainer), repeat(rf_clf), repeat(expected_value))):
            shap_values, raw_values = res
            shap_results.append(shap_values); shap_raw.append(raw_values)
            processed_counter += shap_values.shape[0]
            if (processed_counter != 0) and (processed_counter % save_it == 0) or (processed_counter == len(shap_data_df)):
                print(f'Saving SHAP data after {processed_counter} iterations...')
                shap_save_df = pd.DataFrame(data=np.row_stack(shap_results), columns=list(x_names) + ['Expected_value', 'Sum', 'Prediction_probability', clf_name])
                raw_save_df = pd.DataFrame(data=np.row_stack(shap_raw), columns=list(x_names))
                shap_save_df.to_csv(out_df_shap_path)
                raw_save_df.to_csv(out_df_raw_path)
            print(f'SHAP frame: {processed_counter} / {len(shap_data_df)}...')

    shap_timer.stop_timer()
    stdout_success(msg='SHAP calculations complete', elapsed_time=shap_timer.elapsed_time_str)
    _ = ShapAggregateStatisticsVisualizer(config_path=ini_file_path,
                                          classifier_name=clf_name,
                                          shap_df=shap_save_df,
                                          shap_baseline_value=int(expected_value * 100),
                                          save_path=save_path)


if __name__ == '__main__':
    data_path = '/Users/simon/Desktop/envs/troubleshooting/Nastacia_unsupervised/project_folder/csv/targets_inserted/122_SA_Day_03_20200705T1429.csv'
    data_df = pd.read_csv(data_path, index_col=0)
    clf_names = ['Attack', 'Escape', 'Defensive']
    # data_cols = [x for x in data_df.columns if not 'Probability_' in x]
    # data_cols = [x for x in data_cols if not x is 'Escape']
    # data_cols = [x for x in data_cols if not x is 'Defensive']
    data_df = data_df[list(data_df.columns)[:-2]]

    config = ConfigReader(config_path='/Users/simon/Desktop/envs/troubleshooting/Nastacia_unsupervised/project_folder/project_config.ini')

    x_df = data_df.drop(config.bp_col_names, axis=1)
    y_df = x_df.pop('Attack')

    ini_file_path = '/Users/simon/Desktop/envs/troubleshooting/Nastacia_unsupervised/project_folder/project_config.ini'
    rf_clf = read_df(file_path='/Users/simon/Desktop/envs/troubleshooting/Nastacia_unsupervised/models/generated_models/Attack.sav', file_type='pickle')



    create_shap_log_mp(ini_file_path=ini_file_path,
                    rf_clf=rf_clf,
                    x_df=x_df,
                    y_df=y_df,
                    x_names=x_df.columns,
                    clf_name='Attack',
                    cnt_present=100,
                    cnt_absent=100,
                    save_path='/Users/simon/Desktop/envs/troubleshooting/unsupervised/dr_models',
                    save_it=1000)


# def create_shap_log(self,
#                     ini_file_path: str,
#                     rf_clf: RandomForestClassifier,
#                     x_df: pd.DataFrame,
#                     y_df: pd.DataFrame,
#                     x_names: List[str],
#                     clf_name: str,
#                     cnt_present: int,
#                     cnt_absent: int,
#                     save_path: str,
#                     save_it: int = 100,
#                     save_file_no: Optional[int] = None) -> None:
