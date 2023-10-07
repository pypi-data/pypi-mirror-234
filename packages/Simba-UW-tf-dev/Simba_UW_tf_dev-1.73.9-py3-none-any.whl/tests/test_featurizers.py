import pytest
import numpy as np
import os, glob
from simba.utils.lookups import get_bp_config_code_class_pairs
from simba.utils.read_write import read_config_entry, read_config_file

FEATURE_EXTRACTION_CLASSES = get_bp_config_code_class_pairs()

class TestFeatureExtractors(object):

    @pytest.fixture(params=['../test/data/test_projects/mouse_open_field/project_folder/project_config.ini',
                            '../test/data/test_projects/zebrafish/project_folder/project_config.ini',
                            '../test/data/test_projects/two_c57/project_folder/project_config.ini'])
    def config_path_arg(self, request):
        return request

    def test_featurizers(self,
                         config_path_arg):
        config_path = config_path_arg.param
        config = read_config_file(config_path)
        animal_cnt = read_config_entry(config, 'General settings', 'animal_no', 'int')
        pose_setting = read_config_entry(config, 'create ensemble settings', 'pose_estimation_body_parts', 'str')
        if pose_setting == 'user_defined':
            feature_extractor = FEATURE_EXTRACTION_CLASSES[pose_setting](config_path=config_path)
        elif pose_setting == '8':
            feature_extractor = FEATURE_EXTRACTION_CLASSES[pose_setting][animal_cnt](config_path=config_path)
        else:
            feature_extractor = FEATURE_EXTRACTION_CLASSES[pose_setting](config_path=config_path)
        feature_extractor.run()
        if pose_setting == '4':
            assert len(feature_extractor.out_data.columns) == 165
        elif pose_setting == '16':
            assert len(feature_extractor.out_data.columns) == 546
        assert len(feature_extractor.out_data.columns) == len(feature_extractor.out_data.select_dtypes([np.number]).columns)
        for f in glob.glob(feature_extractor.save_dir + '/*.csv'): os.remove(f)