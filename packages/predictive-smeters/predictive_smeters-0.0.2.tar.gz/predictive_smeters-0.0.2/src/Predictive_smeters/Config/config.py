# Predictive_models.Config.config
import importlib
import os
from configparser import ConfigParser


class Configuration:
    results_dir = os.path.join(os.getcwd(), "Results")

    current_package = __package__.split(".")[0]

    config_dir = "Configuration_files"

    #  Config.ini section and value names
    input_dirs = "directories.data_input"
    output_dirs = "directories.data_output"

    input_datadir_name = "input_datadir"

    def __init__(self):
        self.project_dir = self.get_project_dir()

        self.config_name = "test_dataset" if self.is_testing() and not self.is_imported() else self.current_package
        self.settings = self.get_settings()

        self.config_file = self.get_config_file()
        self.config = self.parser_file()

        self.config_file_main = self.get_config_file(main_file=True)
        self.config_main = self.parser_file(main_file=True)

        self.input_datadir = self.get_input_datadir()

    @staticmethod
    def is_testing():
        return os.path.basename(os.getcwd()) == "tests"

    def is_imported(self):
        return self.get_caller_package() != self.current_package

    def get_project_dir(self):
        return os.path.dirname(os.getcwd()) if self.is_testing() else os.getcwd()

    def get_caller_package(self):
        return os.path.basename(self.get_project_dir())

    def get_settings(self):
        try:
            settings = importlib.import_module(
                f"{__package__}.settings.{self.config_name}_settings").settings()
        except ModuleNotFoundError:
            print(f"Module {self.config_name}_settings not found in {__package__}.settings.")
            settings = {}
        except AttributeError(
                f"No settings dict is found for {self.config_name} so only using default settings"):
            settings = {}

        return settings

    def get_config_file(self, main_file: bool = False):
        file_name = self.get_caller_package() if main_file else self.config_name
        return os.path.join(self.project_dir, self.config_dir, f"{file_name}_config.ini")

    def parser_file(self, main_file: bool = False) -> ConfigParser:
        config_file = self.config_file_main if main_file else self.config_file

        config = ConfigParser()
        config.read(config_file)

        return config

    def get_main_dir(self):
        project_dir = self.config_main.get(self.output_dirs, "project_dir", fallback=None)
        return os.path.join(project_dir, self.config_dir)

    def get_input_datadir(self):
        if self.is_testing() and not self.is_imported():
            return os.path.join(os.getcwd(), "Data")

        if self.is_imported():
            return self.config_main.get(self.input_dirs, self.input_datadir_name, fallback=None)

        if self.config.has_section(self.input_dirs) and self.input_datadir_name in self.config.options(self.input_dirs):
            return self.config.get(self.input_dirs, self.input_datadir_name)

        return r"example\directory"

    def config_func(self):
        self.set_configuration_settings()

        if self.is_testing() and not self.is_imported():  # and self.main_file:
            from Predictive_smeters.Config import TestDataDirs, TestDataFiles
            TestDataDirs().create_test_data_dirs()
            TestDataFiles().create_test_data_files()

        # Data output directories
        for output_dir in self.config.options(self.output_dirs):
            if not os.path.exists(self.config.get(self.output_dirs, output_dir)):
                os.makedirs(self.config.get(self.output_dirs, output_dir))

        self.save_config()
        self.do_configured_directories_exist(configured=True)

    def get_default_dir_settings(self):
        return {self.input_dirs: {self.input_datadir_name: self.input_datadir
                                  },
                self.output_dirs: {"project_dir": self.project_dir,
                                   "results_dir": self.results_dir
                                   }
                }

    def set_configuration_settings(self):
        for section_dic in (self.get_default_dir_settings(), self.settings):
            for section, dic in section_dic.items():
                if not self.config.has_section(section):
                    self.config.add_section(section)

                for key, val in dic.items():
                    print(key, val)
                    self.config.set(section, key, val)

    def do_configured_directories_exist(self, configured: bool = False):
        parser = self.parser_file()
        if not parser.has_section(self.input_dirs) or self.input_datadir_name not in parser.options(self.input_dirs):
            if not configured:
                self.config_func()
            else:
                raise NotADirectoryError(f"{self.input_datadir_name} not in configuration file.")

        input_datadir = parser.get(self.input_dirs, self.input_datadir_name)
        directories = {self.input_datadir_name: input_datadir,
                       **{inp: os.path.join(input_datadir, dir_) for inp, dir_ in parser.items(self.input_dirs)}}
        data_inputs = [inp for inp, dir_ in directories.items() if not os.path.exists(dir_)]
        # data_inputs = [key for key, val in config_obj[self.input_dirs].items() if not os.path.exists(val)]
        if data_inputs:
            if not configured:
                self.config_func()
            else:
                raise NotADirectoryError(f"Warning: Directories in {self.config_file}' need to be configured:"
                                         f"{data_inputs}.")

    def save_config(self):
        if not os.path.exists(os.path.dirname(self.config_file)):
            os.makedirs(os.path.dirname(self.config_file))

        with open(self.config_file, "w") as f:
            self.config.write(f)
