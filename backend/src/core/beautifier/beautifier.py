from io import BytesIO
from typing import Dict, Tuple

import pandas as pd
from pandas import DataFrame, Series


class PhoneNumbersBeautifier:
    def __init__(self, config, project_name):
        self.config = config
        self.project_name = project_name

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
                if self.project_name == "tzb":
                    reason = "это регион, у которого в 'Region-->TZB_Reg_code' стоит 0 в столбце 'Code_region_TZB'"
                elif self.project_name == "os":
                    reason = "это регион, у которого в 'Region-->OS_Region-->OS_Code' стоит 0 в столбце 'Region_Code'"
                tailored_row["reason"] = reason
                ignored_records.append(tailored_row)
                continue

            if self.project_name == "tzb" and not self.check_if_operator_is_allowed_for_TZB(tailored_row):
                tailored_row["reason"] = (
                    "эта комбинация 'регион + оператор' не разрешена," "см. вкладку 'Oper-->Allowed_Region'"
                )
                ignored_records.append(tailored_row)
                continue

            if self.project_name == "tzb" and self.check_if_operator_is_other_for_TZB(tailored_row):
                tailored_row["reason"] = "этот оператор - 'Другие'"
                ignored_records.append(tailored_row)
                continue

            records.append(tailored_row)

        records = pd.DataFrame(records)
        empty_phone_numbers = pd.DataFrame(empty_phone_numbers)
        ignored_records = pd.DataFrame(ignored_records)

        return records, empty_phone_numbers, ignored_records

    def parse_row(self, row: Series) -> Dict[str, str]:
        if self.project_name == "os":
            return self.parse_row_for_os(row)
        elif self.project_name == "tzb":
            return self.parse_row_for_tzb(row)

    def parse_row_for_os(self, row: Series) -> Dict[str, str]:
        return {
            "phone_number": str(row["num"]).replace(" ", ""),
            "region": row["REGION"],
            "operator": row["OPERATOR"],
        }

    def parse_row_for_tzb(self, row: Series) -> Dict[str, str]:
        return {
            "phone_number": str(row["num"]).replace(" ", ""),
            "region": row["REGION"],
            "operator": row["OPERATOR"],
            "Пол": row["Пол"],
            "Возраст": row["Возраст"],
            "iSayMail": row["iSayMail"],
            "Reward": row["Reward"],
        }

    def check_if_region_is_allowed(self, parsed_row: Dict[str, str]) -> bool:
        try:
            self.get_refined_region(parsed_row)
        except KeyError as e:
            return False

        return True

    def make_log_row_for_missing_region(self, parsed_row: Dict[str, str]) -> Dict[str, str]:
        result = {}

        if self.project_name == "os":
            result = self.make_log_row_for_missing_region_for_OS(parsed_row)

        elif self.project_name == "tzb":
            result = self.make_log_row_for_missing_region_for_TZB(parsed_row)

        else:
            raise NotImplementedError

        return result

    def make_log_row_for_missing_region_for_OS(self, parsed_row: Dict[str, str]) -> Dict[str, str]:
        return {
            "Number": parsed_row["phone_number"],
            "DisplayField2": parsed_row["region"],
            "oper": parsed_row["operator"],
            "reason": "Такого региона нет на вкладке 'Region-->OS_Region'",
        }

    def make_log_row_for_missing_region_for_TZB(self, parsed_row: Dict[str, str]) -> Dict[str, str]:
        return {
            "Number": parsed_row["phone_number"],
            "RegionName": parsed_row["region"],
            "OperatorName": parsed_row["operator"],
            "reason": "Такого региона нет на вкладке 'Region-->TZB_Reg_code'",
        }

    def make_tailored_row(self, parsed_row: Dict[str, str]) -> Dict[str, str]:
        result = {}

        if self.project_name == "os":
            result = self.make_tailored_row_for_OS(parsed_row)

        elif self.project_name == "tzb":
            result = self.make_tailored_row_for_TZB(parsed_row)

        else:
            raise NotImplementedError

        return result

    def make_tailored_row_for_OS(self, parsed_row: Dict[str, str]) -> Dict[str, str]:
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

    def make_tailored_row_for_TZB(self, parsed_row: Dict[str, str]) -> Dict[str, str]:
        phone_number = self.try_to_validate_phone_number(parsed_row["phone_number"])
        region = self.get_refined_region(parsed_row)
        operator = self.get_operator(parsed_row)
        interval = self.get_interval(region)
        region_code = self.get_region_code(region)
        operator_code = self.get_operator_code(operator)

        return {
            "Number": phone_number,
            "RegionName": region,
            "OperatorName": operator,
            "TimeDifference": self.get_time_difference(region),
            "Region": region_code,
            "Operator": operator_code,
            "CallIntervalBegin": interval["begin"],
            "CallIntervalEnd": interval["end"],
            "Group": self.get_tzb_group(region, operator),
            "CHECK": self.get_external_id(phone_number),
            "Mark": self.get_tzb_mark(region_code, operator_code),
            "Пол": parsed_row["Пол"],
            "Возраст": parsed_row["Возраст"],
            "iSayMail": parsed_row["iSayMail"],
            "Reward": parsed_row["Reward"],
            "SOURCE": "3",  # A static fixed value required by another program for some reason
        }

    # Try to validate phone number if if can be validated
    def try_to_validate_phone_number(self, phone_number: str) -> str:
        validated_phone_number = phone_number

        if phone_number[:2] == "89" and len(phone_number) == 11:
            validated_phone_number = "7" + phone_number[1:]

        elif phone_number[0] == "9" and len(phone_number) == 10:
            validated_phone_number = "7" + phone_number

        return validated_phone_number

    def check_if_phone_number_is_valid(self, phone_number: str) -> bool:
        if len(phone_number) != 11:
            return False

        if phone_number[0] == "7" and phone_number[1] != "9":
            return False

        if phone_number[0] == "8" and phone_number[1] != "9":
            return False

        if phone_number[0] not in ["7", "8"]:
            return False

        return True

    def get_external_id(self, phone_number: str) -> str:
        return phone_number[-10:]

    def get_refined_region(self, row: Dict) -> str:
        return self.config["regions"][row["region"]]

    def get_region_code(self, region: str) -> str:
        return self.config["region_codes"][region]

    def get_federal_district(self, region: str) -> str:
        return self.config["federal_districts"][region]

    def get_federal_district_code(self, federal_district: str) -> int:
        return self.config["federal_districts_codes"][federal_district]

    def get_filial_code(self, region: str) -> int:
        return self.config["filials"][region]

    def get_operator(self, row: Dict) -> str:
        return self.config["operators"][row["operator"]]

    def get_interval(self, region: str) -> Dict[str, str]:
        return self.config["intervals"][region]

    def get_time_difference(self, region: str) -> str:
        return self.config["time_difference"][region]

    def get_operator_code(self, operator: str) -> str:
        return self.config["operator_codes"][operator]

    def get_tzb_group(self, region: str, operator: str) -> str:
        return f"{region}_{operator}"

    def get_tzb_mark(self, region_code: int, operator_code: int) -> str:
        return f"{region_code}_{operator_code}"

    def check_if_region_is_ignored(self, tailored_row: Dict[str, str]) -> bool:
        if self.project_name == "os":
            return self.check_if_region_is_ignored_for_OS(tailored_row)

        elif self.project_name == "tzb":
            return self.check_if_region_is_ignored_for_TZB(tailored_row)

        else:
            raise NotImplementedError

    def check_if_region_is_ignored_for_OS(self, tailored_row: Dict[str, str]) -> bool:
        if tailored_row["DisplayField2"] in self.config["ignores"]:
            return True

        return False

    def check_if_region_is_ignored_for_TZB(self, tailored_row: Dict[str, str]) -> bool:
        if tailored_row["RegionName"] in self.config["ignores"]:
            return True

        return False

    def check_if_operator_is_allowed_for_TZB(self, tailored_row: Dict[str, str]) -> bool:
        allowed_operator_regions = self.config["allowed_operators"].get(tailored_row["OperatorName"], [])
        if len(allowed_operator_regions) == 0:
            return True

        if tailored_row["RegionName"] in allowed_operator_regions:
            return True

        return False

    def check_if_operator_is_other_for_TZB(self, tailored_row: Dict[str, str]) -> bool:
        if tailored_row["OperatorName"] == "Другие":
            return True

        return False

    def get_refined_quota_region(self, region: str) -> str:
        return self.config["regions"][region]

    def run(self, dataframe: DataFrame) -> Tuple[DataFrame, DataFrame, DataFrame]:
        new_dataset, empty_phone_numbers, ignored_records = self.parse_dataset(dataframe)
        return new_dataset, empty_phone_numbers, ignored_records
