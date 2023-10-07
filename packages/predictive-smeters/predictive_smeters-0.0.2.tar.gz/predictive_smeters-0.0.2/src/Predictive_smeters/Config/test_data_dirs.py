import os

import Predictive_smeters


class TestDataDirs:
    """Defines the directories to use to construct test data files and to be used to test the methods of the
        Predictive_models package.
        """
    def create_test_data_dirs(self):
        if not os.path.exists(Predictive_smeters.Config_obj.input_datadir):
            os.makedirs(Predictive_smeters.Config_obj.input_datadir)