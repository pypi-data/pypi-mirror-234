# Predictive_models.__init__
print(f"Importing {__name__}")

from Predictive_smeters.Config.config import Configuration
Config_obj = Configuration()
Config_obj.do_configured_directories_exist()

from Predictive_smeters.RunModel.model import Model
