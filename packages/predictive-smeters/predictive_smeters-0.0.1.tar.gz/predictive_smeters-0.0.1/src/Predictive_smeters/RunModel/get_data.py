import os

import pandas as pd


class GetData:
    """Class to import and format data ready for the selected model."""

    def data_import(self, file: str, dirpath: str) -> pd.DataFrame:
        """Import csv file to pandas dataframe given file name and directory path."""
        df = pd.read_csv(os.path.join(dirpath, f"{file}.csv"), parse_dates=[0], index_col=[0])

        # Convert index to datetime if it's not already
        if not pd.core.dtypes.common.is_datetime64_any_dtype(df.index):
            df.index = pd.to_datetime(df.index, format="mixed")

        return df

    def data_format(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format data to be processed by selected model."""
        return df
