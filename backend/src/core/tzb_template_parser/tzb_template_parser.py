from typing import Tuple

import pandas as pd
from pandas import DataFrame


class TZBTemplateParser:
    def get_source_from_template(self) -> DataFrame:
        return pd.read_excel(
            "/home/unclemisha/py/phone-numbers-beautifier/xlsx/template/iSay_template.xlsx", sheet_name="Исходник"
        )

    def make_new_source(self, df: DataFrame) -> DataFrame:
        # We get rows between, and including, two dates specified in the interface
        from_date, to_date = self.get_source_date_range("2024-01-09,2024-01-11")
        return df.loc[(df["Дата"] >= f"{from_date} 00:00:00") & (df["Дата"] <= f"{to_date} 00:00:00")]

    def get_source_date_range(self, dates: str) -> Tuple[str, str]:
        return dates[:10], dates[11:]

    def get_source_two_from_template(self) -> DataFrame:
        return pd.read_excel(
            "/home/unclemisha/py/phone-numbers-beautifier/xlsx/template/iSay_template.xlsx", sheet_name="Исходник2"
        )

    def make_new_source_two(self, df: DataFrame) -> DataFrame:
        # We always get rows with the day before yesterday date
        from_date, to_date = self.get_source_two_date_range()
        return df.loc[(df["Дата"] >= f"{self.from_date} 00:00:00") & (df["Дата"] <= f"{self.to_date} 00:00:00")]

    def get_source_two_date_range(self, dates: str) -> Tuple[str, str]:
        return dates[:10], dates[11:]


    def run(self):
        source = self.get_source_from_template()
        new_source = self.make_new_source(source)

        # source_two = self.get_source_two_from_template()
        # new_source_two = self.make_new_source_two(source)


if __name__ == "__main__":
    p = TZBTemplateParser()
    p.run()

