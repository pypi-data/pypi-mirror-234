import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import ElasticNetCV

import Predictive_smeters
from Predictive_smeters.Models.elastic_net_regression import ENR


class Model:
    """Class to implement the sklearn.linear_model package."""
    config = Predictive_smeters.Config_obj.config

    def __init__(self, model_name: str, df: pd.DataFrame):
        self.model_name = model_name
        self.model = self.get_model()
        self.df = df
        self.train_data = None
        self.test_data = None

    def get_model(self):
        if self.model_name in ("ENR", "enr"):
            return ElasticNetCV()

    def get_train_test_set(self) -> pd.DataFrame:
        return self.df  # .loc[self.df.index <= somedate]

    # def get_predict_set(self) -> pd.DataFrame:
    #     return self.df.loc[self.df.index >= somedate2]

    def set_train_test_data(self, test_size: float = 0.5):
        self.train_data, self.test_data = model_selection.train_test_split(self.get_train_test_set(),
                                                                           test_size=test_size)

    def get_train_data(self):
        if self.train_data is None:
            self.set_train_test_data()

        return self.train_data

    def get_test_data(self):
        if self.train_data is None:
            self.set_train_test_data()

        return self.test_data

    def get_X_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(columns=self.config.get("parameters", "dependent_var"))

    def get_y_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.loc[:, self.config.get("parameters", "dependent_var")]

    def train_model(self):
        X = self.get_X_data(self.get_train_data())
        y = self.get_y_data(self.get_train_data())
        self.model.fit(X, y)

    def make_predictions(self, X: np.ndarray):
        return self.model.predict(X)

