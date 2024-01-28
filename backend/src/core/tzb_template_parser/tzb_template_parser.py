from typing import Tuple

import pandas as pd
from pandas import DataFrame, ExcelFile
from typing import Dict


class TZBTemplateParser:
    def get_source_one_from_template(self, excel_file: ExcelFile) -> DataFrame:
        return pd.read_excel(excel_file, sheet_name="Исходник")

    def make_new_source_one(self, df: DataFrame) -> DataFrame:
        # We get rows between, and including, two dates specified in the interface
        from_date, to_date = self.get_source_date_range("2024-01-09,2024-01-11")
        return df.loc[(df["Дата"] >= f"{from_date} 00:00:00") & (df["Дата"] <= f"{to_date} 00:00:00")]

    def get_source_two_from_template(self) -> DataFrame:
        return pd.read_excel(
            "/home/unclemisha/py/phone-numbers-beautifier/xlsx/template/iSay_template.xlsx", sheet_name="Исходник2"
        )

    def make_new_source_two(self, df: DataFrame) -> DataFrame:
        # We always get rows with the day before yesterday date
        from_date, to_date = self.get_source_two_date_range()
        return df.loc[(df["Дата"] >= f"{self.from_date} 00:00:00") & (df["Дата"] <= f"{self.to_date} 00:00:00")]

    def make_new_source_dataframe(self, dates: Dict, excel_file: ExcelFile):
        print("---")
        source_dataframe = self.get_source_one_from_template(excel_file)
        for _, row in source_dataframe.iterrows():
            print(row)
        print("---")
        # new_source = self.make_new_source(source)

        # source_two = self.get_source_two_from_template()
        # new_source_two = self.make_new_source_two(source)


if __name__ == "__main__":
    p = TZBTemplateParser()
    p.run()
