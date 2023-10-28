import json
from datetime import time
from typing import Dict, List, Tuple

import pandas as pd
from pandas import ExcelFile


class ConfigMaker:
    def make_regions_config(self, excel_file: ExcelFile) -> Dict:
        regions = {}

        df = pd.read_excel(excel_file, sheet_name="Region-->OS_Region")

        for _, row in df.iterrows():
            regions[row["Region"].strip()] = row["Region_OS"].strip()

        return regions

    def make_region_codes_config(self, excel_file: ExcelFile) -> Dict:
        region_codes = {}

        df = pd.read_excel(excel_file, sheet_name="OS_Region-->OS_Code")

        for _, row in df.iterrows():
            region_codes[row["Region_OS"]] = int(row["Region_Code"])

        return region_codes

    def make_federal_districts_config(self, excel_file: ExcelFile) -> Dict[str, str]:
        federal_districts = {}
        df = pd.read_excel(excel_file, sheet_name="Obl_OS-->FO_Name")

        for _, row in df.iterrows():
            federal_districts[row["Obl_Os"]] = row["FO_Name"]

        return federal_districts

    def make_federal_districts_codes_config(self, excel_file: ExcelFile) -> Dict[str, str]:
        federal_districts_codes = {}
        df = pd.read_excel(excel_file, sheet_name="FO_Name-->FO_Code")

        for _, row in df.iterrows():
            federal_districts_codes[row["FO_Name"]] = row["FO_Code"]

        return federal_districts_codes

    def make_filials_config(self, excel_file: ExcelFile) -> Dict[str, str]:
        filials = {}

        df = pd.read_excel(excel_file, sheet_name="OS_Obl-->filial")

        for _, row in df.iterrows():
            filials[row["Obl_OS"]] = row["mgFil_Code"]

        return filials

    def make_operators_config(self, excel_file: ExcelFile) -> Dict[str, str]:
        operators = {}

        df = pd.read_excel(excel_file, sheet_name="Oper-->OS_Oper_Code")

        for _, row in df.iterrows():
            operators[row["OPERATOR"]] = row["Code"]

        return operators

    def make_intervals_config(self, excel_file: ExcelFile) -> Dict[str, Dict[str, str]]:
        intervals = {}

        df = pd.read_excel(excel_file, sheet_name="OS_Region-->Interval")

        for _, row in df.iterrows():
            intervals[row["Obl_OS"]] = {
                "begin": self.convert_time_to_string(row["CallIntervalBegin"]),
                "end": self.convert_time_to_string(row["CallIntervalEnd"]),
            }

        return intervals

    def make_ignore_config(self, excel_file: ExcelFile) -> List[str]:
        ignore = []

        df = pd.read_excel(excel_file, sheet_name="OS_Region-->OS_Code")

        for _, row in df.iterrows():
            if row["Region_Code"] == 0:
                ignore.append(row["Region_OS"])

        return ignore

    def convert_time_to_string(self, time: time) -> str:
        if pd.isna(time):
            return ""

        return time.strftime("%H:%M:%S")

    def make_config_file(self, excel_file: ExcelFile) -> Dict:
        config = {}

        config["regions"] = self.make_regions_config(excel_file)
        config["region_codes"] = self.make_region_codes_config(excel_file)
        config["federal_districts"] = self.make_federal_districts_config(excel_file)
        config["federal_districts_codes"] = self.make_federal_districts_codes_config(excel_file)
        config["filials"] = self.make_filials_config(excel_file)
        config["operators"] = self.make_operators_config(excel_file)
        config["intervals"] = self.make_intervals_config(excel_file)
        config["ignores"] = self.make_ignore_config(excel_file)

        return config
