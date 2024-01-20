from typing import Dict, Tuple

import pandas as pd
from pandas import DataFrame, Series

from src.core.beautifier.beautifier import PhoneNumbersBeautifier


class PhoneNumbersBeautifierOS(PhoneNumbersBeautifier):
    def __init__(self, config):
        super().__init__(config)

    def parse_dataset(self, dataframe: DataFrame) -> Tuple[DataFrame, DataFrame, DataFrame]:
        records = []
        empty_phone_numbers = []
        ignored_records = []

        for _, row in dataframe.iterrows():
            if pd.isna(row["REGION"]):
                empty_phone_numbers.append(row["num"])
                continue

            parsed_row = self.parse_row(row)

            if not self.check_if_region_is_allowed(parsed_row):
                log_row = self.make_log_row_for_missing_region(parsed_row)
                ignored_records.append(log_row)
                continue

            tailored_row = self.make_tailored_row(parsed_row)

            if not self.check_if_phone_number_is_valid(tailored_row["Number"]):
                empty_phone_numbers.append(row["num"])
                continue

            if self.check_if_region_is_ignored(tailored_row):
                tailored_row[
                    "reason"
                ] = "это регион, у которого в 'Region-->OS_Region-->OS_Code' стоит 0 в столбце 'Region_Code'"
                ignored_records.append(tailored_row)
                continue

            records.append(tailored_row)

        records = pd.DataFrame(records)
        empty_phone_numbers = pd.DataFrame(empty_phone_numbers)
        ignored_records = pd.DataFrame(ignored_records)

        return records, empty_phone_numbers, ignored_records

    def parse_row(self, row: Series) -> Dict[str, str]:
        return {
            "phone_number": str(row["num"]).replace(" ", ""),
            "region": row["REGION"],
            "operator": row["OPERATOR"],
        }

    def check_if_region_is_ignored(self, tailored_row: Dict[str, str]) -> bool:
        if tailored_row["DisplayField2"] in self.config["ignores"]:
            return True

        return False

    def make_log_row_for_missing_region(self, parsed_row: Dict[str, str]) -> Dict[str, str]:
        return {
            "Number": parsed_row["phone_number"],
            "DisplayField2": parsed_row["region"],
            "oper": parsed_row["operator"],
            "reason": "Такого региона нет на вкладке 'Region-->OS_Region'",
        }

    def make_tailored_row(self, parsed_row: Dict[str, str]) -> Dict[str, str]:
        phone_number = self.try_to_validate_phone_number(parsed_row["phone_number"])
        region = self.get_refined_region(parsed_row)
        federal_district = self.get_federal_district(region)
        interval = self.get_interval(region)

        return {
            "Number": phone_number,
            "ВнешнийID": self.get_external_id(phone_number),
            "DisplayField1": federal_district,
            "DisplayField2": region,
            "DisplayField3": self.get_federal_district_code(federal_district),
            "filial": self.get_filial_code(region),
            "obl": self.get_region_code(region),
            "CallIntervalBegin": interval["begin"],
            "CallIntervalEnd": interval["end"],
            "oper": self.get_operator(parsed_row),
            "Mark": self.get_region_code(region),
        }
