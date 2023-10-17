import pandas as pd
import glob

DATA_DIRECTORY = r'/Users/simon/Desktop/envs/troubleshooting/one_black_animal/project_folder/csv/targets_inserted/'
CLASSIFIER_NAME = 'My_classifier'

file_paths = glob.glob(DATA_DIRECTORY + '/*.csv')
error_file_count = 0
for file_path in file_paths:
    df = pd.read_csv(file_path)
    if CLASSIFIER_NAME not in df.columns:
        print(f'ERROR: In file {file_path}, {CLASSIFIER_NAME} column does not exist ')
        error_file_count += 1
        continue
    unique_entries = df[CLASSIFIER_NAME].astype(str).unique().tolist()
    unaccepted_entries = [x for x in unique_entries if x not in ['0', '1']]
    if len(unaccepted_entries) > 0:
        print(f'ERROR: Column {CLASSIFIER_NAME} in file {file_path} has {len(unaccepted_entries)} unaccepted entries: {unaccepted_entries}.')
        error_file_count += 1

print(f'COMPLETE: {error_file_count} error(s) found')






