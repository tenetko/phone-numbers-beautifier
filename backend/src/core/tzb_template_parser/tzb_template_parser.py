from datetime import datetime
from typing import Dict, Tuple

import pandas as pd
import pytz
from pandas import DataFrame, ExcelFile


class TZBTemplateParser:
    def get_source_one_from_template(self, excel_file: ExcelFile) -> DataFrame:
        return pd.read_excel(excel_file, sheet_name="Исходник")

    def get_source_two_from_template(self, excel_file: ExcelFile) -> DataFrame:
        return pd.read_excel(excel_file, sheet_name="Исходник2")

    def get_date(self, raw_date_time: str) -> str:
        # Mon, 01 Jan 2024 16:37:02 GMT --> 2024-01-01
        date_time = self.convert_date_time_to_moscow_timezone(raw_date_time)

        return self.get_date_from_date_time(date_time)

    def convert_date_time_to_moscow_timezone(self, raw_date_time: str) -> datetime:
        # Mon, 01 Jan 2024 16:37:02 GMT --> 2024-01-01 19:37:02
        date_time = datetime.strptime(raw_date_time, "%a, %d %b %Y %H:%M:%S %Z")
        date_time = pytz.utc.localize(date_time)
        date_time = date_time.astimezone(pytz.timezone("Europe/Moscow"))

        return date_time

    def get_date_from_date_time(self, date_time: datetime) -> str:
        # 2024-01-01 19:37:02 --> 2024-01-01
        return datetime.strftime(date_time, "%Y-%m-%d")

    def make_filtered_source_dataframe(self, dataframe: DataFrame, date_from, date_to) -> DataFrame:
        # We get rows between, and including, two dates specified in the interface
        result = dataframe.loc[
            (dataframe["Дата"] >= f"{date_from} 00:00:00") & (dataframe["Дата"] <= f"{date_to} 00:00:00")
        ].copy()
        result.reset_index(inplace=True, drop=True)

        return result

    def make_merged_source_dataframe(self, dates: Dict, excel_file: ExcelFile):
        merged_source_dataframe = DataFrame()

        source_dataframe = self.get_source_one_from_template(excel_file)
        date_from = self.get_date(dates["source_1_date_0"])
        date_to = self.get_date(dates["source_1_date_1"])
        source_one = self.make_filtered_source_dataframe(source_dataframe, date_from, date_to)

        source_dataframe = self.get_source_two_from_template(excel_file)
        date_from = self.get_date(dates["source_2_date_0"])
        date_to = self.get_date(dates["source_2_date_1"])
        source_two = self.make_filtered_source_dataframe(source_dataframe, date_from, date_to)

        source_one["Source"] = pd.Series(["source_one"] * len(source_one.index))
        source_two["Source"] = pd.Series(["source_two"] * len(source_two.index))

        merged_source_dataframe = pd.concat([source_one, source_two])
        merged_source_dataframe.reset_index(inplace=True, drop=True)

        return merged_source_dataframe
