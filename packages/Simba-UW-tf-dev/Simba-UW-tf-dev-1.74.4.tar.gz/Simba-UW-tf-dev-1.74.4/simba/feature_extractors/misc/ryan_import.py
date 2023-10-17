import os
import csv
from tqdm import tqdm
from simba.data_processors.interpolation_smoothing import AdvancedSmoother
from simba.data_processors.interpolation_smoothing import AdvancedInterpolator
from simba.outlier_tools.outlier_corrector_movement_advanced import OutlierCorrecterMovementAdvanced
from simba.outlier_tools.outlier_corrector_location_advanced import OutlierCorrecterLocationAdvanced
# from simba.utils.cli.cli_tools import set_video_parameters
from simba.mixins.config_reader import ConfigReader
from simba.utils.read_write import find_files_of_filetypes_in_directory, write_df, copy_multiple_videos_to_project, \
    copy_single_video_to_project, find_core_cnt, read_config_entry, read_config_file
from simba.utils.data import slp_to_df_convert
from simba.utils.read_write import get_fn_ext

# from simba.data_processors.interpolation_smoothing import Smooth, Interpolate

# DEFINE THE DIRECTORY CONTAINING YOUR SLEAP DATA IN H5 FORMAT AND THE PATH TO YOUR SIMBA PROJECT CONFIG
project_name = "dam_nest-c-only"
BASE_DIR = '/Users/simon/Desktop/envs/troubleshooting/ryan_dam_nest'
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_Path = os.path.join(BASE_DIR, "csv", "input_csv")
CONFIG_PATH = os.path.join(BASE_DIR, "project_folder", "project_config.ini")
vid_csv_path = os.path.join(os.path.dirname(CONFIG_PATH), "logs", "video_info.csv")
#VID_DIR = r"R:\Basic_Sciences\Phys\Lerner_Lab_tnl2633\Ryan\camera_stuff\video\Selected.for.training\cut 9.5.2023"
# VID_DIR = r"C:\Users\RFK\Documents\sleap_coding"
VID_DIR = r"/Users/simon/Desktop/envs/troubleshooting/ryan_dam_nest/videos"


# video settings
fps = 30
px_per_mm = 0.94286
resolution = (512, 288)  # WIDTH X HEIGHT
distance = 330

# Import option, default should be None... this is dropping empty bps after merging different skeletons in sleap
drop_body_parts = ['nest_c_1', 'd_nose_2', 'd_neck_2', 'd_back_2', 'd_tail_2']
# Interpolation
TYPE = 'animal'
INTERPOLATION_SETTINGS = {'Animal_1': 'quadratic', 'Animal_2': 'nearest'}
# quadratic, linear, or nearest
SMOOTHING_SETTINGS = {'Animal_1': {'method': 'Savitzky Golay', 'time_window': 100},
                      'Animal_2': {'method': 'Gaussian', 'time_window': 3000}}
MULTI_INDEX_INPUT = True
OVERWRITE = True

# Outlier correction
AGG_METHOD = 'median'
CRITERION_BODY_PARTS = {'Animal_1': ['d_neck_1', 'd_tail_1']}  # omit nest in nest-c-only
# CRITERION_BODY_PARTS={'Animal_1': ['d_neck', 'd_tail'], 'Animal_2': ['nest_bl', 'nest_tr']}
SETTINGS = {'Animal_1': 2.25}  # omit nest in nest-c-only
# SETTINGS={'Animal_1': 2, 'Animal_2': 3}


# READ IN THE SIMBA PROJECT CONFIG AND FIND THE H5 PATHS INSIDE THE DATA_DIR
config = ConfigReader(config_path=CONFIG_PATH, read_video_info=False)
data_files = find_files_of_filetypes_in_directory(directory=DATA_DIR, extensions=['.h5'], raise_error=True)

for file_path in tqdm(data_files):
    # file_path=data_files[0]
    vid_ext = os.path.basename(file_path)
    vid_no_ext, _ = os.path.splitext(vid_ext)
    vid_path = os.path.join(VID_DIR, vid_no_ext + '.mp4')
    copy_single_video_to_project(simba_ini_path=CONFIG_PATH, source_path=vid_path, symlink=True, overwrite=True)

    # this isn't working but it is where I'm at... possibly make a  thing to add to the project_folder/logs/video_info.csv file
    # set_video_parameters(config_path=CONFIG_PATH, px_per_mm=PX_PER_MM, fps=FPS, resolution=RESOLUTION)

    # Add a new row to the CSV file
    _, video_name, _ = get_fn_ext(filepath=file_path)
    print(f'Importing {video_name}...')
    file_exists = os.path.exists(vid_csv_path)
    with open(vid_csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # If the file is empty (no header), add the header
            writer.writerow(["Video", "fps", "Resolution_width", "Resolution_height", "Distance_in_mm", "pixels/mm"])

        # Add the new row with the provided values
        writer.writerow([video_name, fps, resolution[0], resolution[1], distance, px_per_mm])

    # CHANGE THE save_path

    # df = slp_to_df_convert(file_path=file_path, headers=config.bp_col_names, joined_tracks=True)
    df = slp_to_df_convert(file_path=file_path, headers=config.bp_col_names, joined_tracks=True, drop_body_parts=drop_body_parts)
    save_path = os.path.join(config.input_csv_dir, f'{video_name}.csv')
    temp_dir = os.path.join(config.input_csv_dir, 'temp_dir')
    temp_file_path = os.path.join(temp_dir, f'{video_name}.csv')
    os.makedirs(temp_dir) if not os.path.exists(temp_dir) else None
    write_df(df=df, file_type='csv', save_path=temp_file_path, multi_idx_header=True)

# Run interpolation if `interpolation_method` is not "None"
interpolator = AdvancedInterpolator(data_dir=temp_dir,
                                    config_path=CONFIG_PATH,
                                    type=TYPE,
                                    settings=INTERPOLATION_SETTINGS,
                                    initial_import_multi_index=MULTI_INDEX_INPUT,
                                    overwrite=OVERWRITE)
interpolator.run()
# Run smoothing if `smoothing_method['Method']` is not "None"
smoother = AdvancedSmoother(data_dir=temp_dir,
                            config_path=CONFIG_PATH,
                            type=TYPE,
                            settings=SMOOTHING_SETTINGS,
                            initial_import_multi_index=True,
                            overwrite=OVERWRITE)
smoother.run()
movement_outlier_corrector = OutlierCorrecterMovementAdvanced(config_path=CONFIG_PATH,
                                                              input_dir=temp_dir,
                                                              criterion_body_parts=CRITERION_BODY_PARTS,
                                                              type=TYPE,
                                                              agg_method=AGG_METHOD,
                                                              settings=SETTINGS)
movement_outlier_corrector.run()
os.rename(temp_file_path, os.path.join(config.input_csv_dir, f'{video_name}.csv'))
print(f'Complete: {video_name}...')