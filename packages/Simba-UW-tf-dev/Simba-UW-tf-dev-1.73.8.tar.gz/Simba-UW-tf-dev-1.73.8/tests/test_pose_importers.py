import pytest
import os, glob
from unittest.mock import Mock

from simba.pose_importers.dlc_importer_csv import import_dlc_csv
from simba.pose_importers.madlc_importer import MADLCImporterH5
from simba.utils.checks import check_file_exist_and_readable

@pytest.mark.parametrize("config_path, source", [('/Users/simon/Desktop/envs/simba_dev/tests/data/test_projects/two_c57/project_folder/project_config.ini',
                                                  '/Users/simon/Desktop/envs/simba_dev/tests/data/test_projects/two_c57/import_csv_dlc_2_line_headers')])
def test_import_dlc_csv(config_path, source):
    results = import_dlc_csv(config_path=config_path, source=source)
    for i in results:
        check_file_exist_and_readable(file_path=i)
        os.remove(i)

    import_files = glob.glob(source + '/*.csv')
    for i in import_files:
        results = import_dlc_csv(config_path=config_path, source=i)
        for j in results:
            check_file_exist_and_readable(file_path=j)
            os.remove(j)

#@pytest.mark.parametrize("config_path, source", [('/Users/simon/Desktop/envs/simba_dev/tests/data/test_projects/two_c57/project_folder/project_config.ini',
#                                                  '/Users/simon/Desktop/envs/simba_dev/tests/data/test_projects/two_c57/import_h5_madlc')])
# def test_MADLCImporterH5(config_path, source):
#     interpolation_settings = 'None'
#     smoothing_settings = {'Method': None}
#     MADLCImporterH5 = Mock()
#
#
#
#     datetime.datetime.today.return_value = tuesday
#     importer = MADLCImporterH5(config_path=config_path,
#                                data_folder=source,
#                                file_type='ellipse',
#                                id_lst=['Simon', 'JJ'],
#                                interpolation_settings=interpolation_settings,
#                                smoothing_settings=smoothing_settings)
#     i
#     importer.run()




# test = MADLCImporterH5(config_path=r'/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini',
#                    data_folder=r'/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/h5',
#                    file_type='ellipse',
#                    id_lst=['Simon', 'JJ'],
#                    interpolation_settings='Body-parts: Nearest',
#                    smoothing_settings = {'Method': 'Savitzky Golay', 'Parameters': {'Time_window': '200'}})
# test.run()