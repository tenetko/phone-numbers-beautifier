from typing import List, Tuple

import pandas as pd
from pandas import DataFrame


class TZBChecker:
    def __init__(self, check_list_dataframe):
        self.check_list_dataframe = check_list_dataframe

    def get_check_list(self) -> List[int]:
        check_list = []
        for _, row in self.check_list_dataframe.iterrows():
            check_list.append(int(row["number"]))

        return check_list

    def check_source(self, source_dataframe: DataFrame) -> Tuple[DataFrame, DataFrame]:
        checked_source_dataframe = source_dataframe.copy(deep=True)
        check_list = self.get_check_list()
        completed = []

        for index, row in checked_source_dataframe.iterrows():
            if int(row["Номер телефона"]) in check_list:
                completed.append(row)
                checked_source_dataframe.drop(index, inplace=True)

        completed_dataframe = pd.DataFrame(completed)
        completed_dataframe.reset_index(inplace=True, drop=True)

        checked_source_dataframe.reset_index(inplace=True, drop=True)

        return checked_source_dataframe, completed_dataframe
