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

    def make_merged_source_dataframe(self, excel_file: ExcelFile):
        merged_source_dataframe = DataFrame()

        source_one = self.get_source_one_from_template(excel_file)
        source_two = self.get_source_two_from_template(excel_file)

        source_one["Source"] = pd.Series(["source_one"] * len(source_one.index))
        source_two["Source"] = pd.Series(["source_two"] * len(source_two.index))

        merged_source_dataframe = pd.concat([source_one, source_two])
        merged_source_dataframe.reset_index(inplace=True, drop=True)

        return merged_source_dataframe
