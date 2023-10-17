import os
from simba.mixins.config_reader import ConfigReader
from simba.utils.read_write import find_files_of_filetypes_in_directory, write_df
from simba.utils.data import slp_to_df_convert
from simba.utils.read_write import get_fn_ext
from simba.data_processors.interpolation_smoothing import Smooth, Interpolate

### DEFINE THE DIRECTORY CONTAINING YOUR SLEAP DATA IN H5 FORMAT AND THE PATH TO YOUR SIMBA PROJECT CONFIG
DATA_DIR = '/Users/simon/Desktop/envs/troubleshooting/sleap_dam_roi/data'
CONFIG_PATH = '/Users/simon/Desktop/envs/troubleshooting/sleap_dam_roi/project_folder/project_config.ini'

# READ IN THE SIMBA PROJECT CONFIG AND THE H5 PATHS INSIDE THE DATA_DIR
config = ConfigReader(config_path=CONFIG_PATH, read_video_info=False)
data_files = find_files_of_filetypes_in_directory(directory=DATA_DIR, extensions=['.h5'], raise_error=True)

#SPECIFY SMOOTHING AND INTERPOLATION SETTINGS
interpolation_method = 'Body-parts: Nearest' # Set to "None" if interpolation should be skipped
smoothing_method = {'Method': 'Savitzky Golay', 'Parameters': {'Time_window': '200'}}

# FOR EVERY H5 FILE FOUND IN THE DATA_DIR, WE (i) CONVERT IT TO A DATAFRAME AND APPEND THE HEADERS AS DEFINED IN THE SIMBA PROJECT, AND
# (ii) SAVE THE DATAFRAME IN THE SIMBA PROJECT `project_folder/csv/input_csv` directory.
for file_path in data_files:
    _, video_name, _ = get_fn_ext(filepath=file_path)
    print(f'Importing {video_name}...')
    df = slp_to_df_convert(file_path=file_path, headers=config.bp_col_names, joined_tracks=True)
    save_path = os.path.join(config.input_csv_dir, f'{video_name}.csv')
    write_df(df=df, file_type='csv', save_path=save_path, multi_idx_header=True)

    #Run interpolation if `interpolation_method` is not None
    if interpolation_method != 'None':
        Interpolate(input_path=save_path,
                    config_path=CONFIG_PATH,
                    method=interpolation_method,
                    initial_import_multi_index=True)

    # Run smoothing if `smoothing_method['Method']` is not None
    if smoothing_method['Method'] != 'None':
        Smooth(config_path=CONFIG_PATH,
               input_path=save_path,
               time_window=int(smoothing_method['Parameters']['Time_window']),
               smoothing_method=smoothing_method['Method'],
               initial_import_multi_index=True)

    print(f'Complete: {video_name}...')
