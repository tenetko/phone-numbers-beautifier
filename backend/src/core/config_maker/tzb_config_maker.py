from collections import defaultdict
from datetime import time
from io import BytesIO
from typing import Dict, List

import pandas as pd
from pandas import ExcelFile


class ConfigMaker:
    def make_regions_config(self, excel_file: ExcelFile) -> Dict[str, str]:
        regions = {}

        df = pd.read_excel(excel_file, sheet_name="Region-->TZB_Reg_code")

        for _, row in df.iterrows():
            regions[row["Unnamed: 0"].strip()] = row["из проекта ТЗБ"].strip()

        return regions

    def make_region_codes_config(self, excel_file: ExcelFile) -> Dict[str, int]:
        region_codes = {}

        df = pd.read_excel(excel_file, sheet_name="Region-->TZB_Reg_code")

        for _, row in df.iterrows():
            if pd.isna(row["Code_region_TZB"]):
                continue

            region_codes[row["Region_TZB"]] = int(row["Code_region_TZB"])

        return region_codes

    def make_operators_config(self, excel_file: ExcelFile) -> Dict[str, str]:
        operators = {}

        df = pd.read_excel(excel_file, sheet_name="Oper-->TZB_Oper_Code")

        for _, row in df.iterrows():
            operators[row["OPERATOR"]] = row["GrM_Name"]

        return operators

    def make_operator_codes_config(self, excel_file: ExcelFile) -> Dict[str, int]:
        operator_codes = {}

        df = pd.read_excel(excel_file, sheet_name="Oper-->TZB_Oper_Code")

        for _, row in df.iterrows():
            if pd.isna(row["GrS_Name"]):
                continue

            operator_codes[row["GrS_Name"]] = int(row["GrS_Code"])

        return operator_codes

    def make_time_difference_config(self, excel_file: ExcelFile) -> Dict[str, str]:
        time_difference_config = {}

        df = pd.read_excel(excel_file, sheet_name="Region-->UTC")

        for _, row in df.iterrows():
            time_difference_config[row["RegionName"]] = row["TimeDifference"]

        return time_difference_config

    def make_intervals_config(self, excel_file: ExcelFile) -> Dict[str, Dict[str, str]]:
        intervals = {}

        df = pd.read_excel(excel_file, sheet_name="Region-->Interval")

        for _, row in df.iterrows():
            intervals[row["RegionName"]] = {
                "begin": self.convert_time_to_string(row["CallIntervalBegin"]),
                "end": self.convert_time_to_string(row["CallIntervalEnd"]),
            }

        return intervals

    def convert_time_to_string(self, time: time) -> str:
        if pd.isna(time):
            return ""

        return time.strftime("%H:%M:%S")

    def make_ignore_config(self, excel_file: ExcelFile) -> List[str]:
        ignore = []

        df = pd.read_excel(excel_file, sheet_name="Region-->TZB_Reg_code")

        for _, row in df.iterrows():
            if row["Code_region_TZB"] == 0:
                ignore.append(row["Region_TZB"])

        return ignore

    def make_allowed_operators_config(self, excel_file: ExcelFile) -> Dict[str, list]:
        allowed_operators = defaultdict(list)

        df = pd.read_excel(excel_file, sheet_name="Oper-->Allowed_Region")

        for _, row in df.iterrows():
            allowed_operators[row["OPERATOR"]].append(row["REGION"])

        return allowed_operators

    def make_config_file(self, excel_file: ExcelFile) -> Dict:
        config = {}

        config["regions"] = self.make_regions_config(excel_file)
        config["region_codes"] = self.make_region_codes_config(excel_file)
        config["operators"] = self.make_operators_config(excel_file)
        config["operator_codes"] = self.make_operator_codes_config(excel_file)
        config["time_difference"] = self.make_time_difference_config(excel_file)
        config["intervals"] = self.make_intervals_config(excel_file)
        config["ignores"] = self.make_ignore_config(excel_file)
        config["allowed_operators"] = self.make_allowed_operators_config(excel_file)

        return config
