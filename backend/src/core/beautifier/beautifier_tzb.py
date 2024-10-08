from typing import Dict, Tuple

import pandas as pd
from pandas import DataFrame, Series

from src.core.beautifier.beautifier import PhoneNumbersBeautifier


class PhoneNumbersBeautifierTZB(PhoneNumbersBeautifier):
    def __init__(self, config):
        super().__init__(config)

    def parse_dataset(self, dataframe: DataFrame) -> Tuple[DataFrame, DataFrame, DataFrame]:
        records = []
        empty_phone_numbers = []
        ignored_records = []

        for _, row in dataframe.iterrows():
            if pd.isna(row["Регион"]):
                empty_phone_numbers.append(row["Номер телефона"])
                continue

            parsed_row = self.parse_row(row)

            if not self.check_if_region_is_allowed(parsed_row):
                log_row = self.make_log_row_for_missing_region(parsed_row)
                ignored_records.append(log_row)
                continue

            tailored_row = self.make_tailored_row(parsed_row)

            if not self.check_if_phone_number_is_valid(tailored_row["Number"]):
                empty_phone_numbers.append(row["Номер телефона"])
                continue

            if self.check_if_region_is_ignored(tailored_row):
                tailored_row[
                    "reason"
                ] = "это регион, у которого в 'Region-->TZB_Reg_code' стоит 0 в столбце 'Code_region_TZB'"
                ignored_records.append(tailored_row)
                continue

            if not self.check_if_operator_is_allowed(tailored_row):
                tailored_row["reason"] = (
                    "эта комбинация 'регион + оператор' не разрешена," "см. вкладку 'Oper-->Allowed_Region'"
                )
                ignored_records.append(tailored_row)
                continue

            if self.check_if_operator_is_other(tailored_row):
                tailored_row["reason"] = "этот оператор - 'Другие'"
                ignored_records.append(tailored_row)
                continue

            records.append(tailored_row)

        records = pd.DataFrame(records)
        empty_phone_numbers = pd.DataFrame(empty_phone_numbers)
        ignored_records = pd.DataFrame(ignored_records)

        return records, empty_phone_numbers, ignored_records

    def parse_row(self, row: Series) -> Dict[str, str]:
        return {
            "phone_number": str(int(row["Номер телефона"])).replace(" ", ""),
            "region": row["Регион"],
            "operator": row["Оператор сотовой связи"],
            "Пол": row["Пол"],
            "Возраст": row["Возраст"],
            "iSayMail": row["Email"],
            "Reward": row["Обещанная награда"],
            "Source": row["Source"],
        }

    def check_if_region_is_ignored(self, tailored_row: Dict[str, str]) -> bool:
        if tailored_row["RegionName"] in self.config["ignores"]:
            return True

        return False

    def make_log_row_for_missing_region(self, parsed_row: Dict[str, str]) -> Dict[str, str]:
        return {
            "Number": parsed_row["phone_number"],
            "RegionName": parsed_row["region"],
            "OperatorName": parsed_row["operator"],
            "reason": "Такого региона нет на вкладке 'Region-->TZB_Reg_code'",
        }

    def make_tailored_row(self, parsed_row: Dict[str, str]) -> Dict[str, str]:
        phone_number = self.try_to_validate_phone_number(parsed_row["phone_number"])
        region = self.get_refined_region(parsed_row)
        operator = self.get_operator(parsed_row)
        region_code = self.get_region_code(region)
        operator_code = self.get_operator_code(operator)
        time_difference = self.get_time_difference(region)

        return {
            "Number": phone_number,
            "RegionName": region,
            "OperatorName": operator,
            "TimeDifference": time_difference,
            "Region": region_code,
            "Operator": operator_code,
            "CallIntervalBegin": "10:00:00",
            "CallIntervalEnd": "22:00:00",
            "Group": self.get_tzb_group(region, operator, parsed_row["Source"]),
            "CHECK": self.get_external_id(phone_number),
            "Mark": self.get_tzb_mark(region_code, operator_code),
            "Пол": parsed_row["Пол"],
            "Возраст": parsed_row["Возраст"],
            "iSayMail": parsed_row["iSayMail"],
            "Reward": parsed_row["Reward"],
            "SOURCE": "3",  # A static fixed value required by another program for some reason
            "TimeZone": self.get_timezone(time_difference),
        }

    def check_if_operator_is_allowed(self, tailored_row: Dict[str, str]) -> bool:
        allowed_operator_regions = self.config["allowed_operators"].get(tailored_row["OperatorName"], [])
        if len(allowed_operator_regions) == 0:
            return True

        if tailored_row["RegionName"] in allowed_operator_regions:
            return True

        return False

    def check_if_operator_is_other(self, tailored_row: Dict[str, str]) -> bool:
        if tailored_row["OperatorName"] == "Другие":
            return True

        return False

    def get_tzb_group(self, region: str, operator: str, source: str) -> str:
        if source == "source_one":
            return f"{region}_{operator}_iSay"
        elif source == "source_two":
            return f"{region}_{operator}_iSay_replay"

    def get_tzb_mark(self, region_code: str, operator_code: str) -> str:
        return f"{region_code}_{operator_code}"

    def get_timezone(self, time_difference: str) -> str:
        return self.config["timezones"][time_difference]
