from typing import List, Tuple

import pandas as pd
from loguru import logger
from pandas import DataFrame

from src.utils.logging.logging import Sink


class TZBFilter:
    def __init__(self, check_list_dataframe: DataFrame, macros_dataframe: DataFrame):
        self.check_list_dataframe = check_list_dataframe
        self.macros_dataframe = macros_dataframe
        self.logs = Sink()
        logger.add(sink=self.logs, serialize=True)

    def get_check_list(self) -> List[int]:
        check_list = []
        for _, row in self.check_list_dataframe.iterrows():
            check_list.append(int(row["number"]))

        return check_list

    def filter_with_checklist(self, source_dataframe: DataFrame) -> Tuple[DataFrame, DataFrame]:
        checked_source_dataframe = source_dataframe.copy(deep=True)
        check_list = self.get_check_list()
        completed = []

        for index, row in checked_source_dataframe.iterrows():
            try:
                if int(row["Номер телефона"]) in check_list:
                    completed.append(row)
                    checked_source_dataframe.drop(index, inplace=True)
            except KeyError:
                logger.exception(f"The source dataframe does not have a column named 'Номер телефона'.")
                raise KeyError

        completed_dataframe = pd.DataFrame(completed)
        completed_dataframe.reset_index(inplace=True, drop=True)

        checked_source_dataframe.reset_index(inplace=True, drop=True)

        return checked_source_dataframe, completed_dataframe

    def get_macros_list(self) -> List[int]:
        check_list = []
        for _, row in self.macros_dataframe.iterrows():
            check_list.append(int(row["num"]))

        return check_list

    def filter_with_macros(self, checked_source_dataframe: DataFrame) -> DataFrame:
        check_list = self.get_macros_list()

        for index, row in checked_source_dataframe.iterrows():
            try:
                if int(row["Номер телефона"]) in check_list:
                    continue
                else:
                    checked_source_dataframe.drop(index, inplace=True)
            except KeyError:
                logger.exception(f"The source dataframe does not have a column named 'Номер телефона'.")
                raise KeyError

        checked_source_dataframe.reset_index(inplace=True, drop=True)

        return checked_source_dataframe
