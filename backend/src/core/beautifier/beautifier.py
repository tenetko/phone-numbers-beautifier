from typing import Dict, Tuple

from loguru import logger
from pandas import DataFrame, Series

from src.utils.logging.logging import Sink


class PhoneNumbersBeautifier:
    def __init__(self, config: Dict):
        self.config = config
        self.logs = Sink()
        logger.add(sink=self.logs, serialize=True)

    def parse_dataset(self, dataframe: DataFrame) -> Tuple[DataFrame, DataFrame, DataFrame]:
        raise NotImplementedError

    def parse_row(self, row: Series) -> Dict[str, str]:
        raise NotImplementedError

    def check_if_region_is_allowed(self, parsed_row: Dict[str, str]) -> bool:
        try:
            self.get_refined_region(parsed_row)
        except KeyError as e:
            return False

        return True

    def make_log_row_for_missing_region(self, parsed_row: Dict[str, str]) -> Dict[str, str]:
        raise NotImplementedError

    def make_tailored_row(self, parsed_row: Dict[str, str]) -> Dict[str, str]:
        raise NotImplementedError

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
        try:
            return self.config["operators"][row["operator"]]
        except KeyError:
            logger.exception(
                f"Phone number {row['phone_number']} has empty 'OPERATOR' value after extending the macros with the source"
            )

    def get_interval(self, region: str) -> Dict[str, str]:
        return self.config["intervals"][region]

    def get_time_difference(self, region: str) -> str:
        return self.config["time_difference"][region]

    def get_operator_code(self, operator: str) -> str:
        return self.config["operator_codes"][operator]

    def check_if_region_is_ignored(self, tailored_row: Dict[str, str]) -> bool:
        raise NotImplementedError

    def get_refined_quota_region(self, region: str) -> str:
        return self.config["regions"][region]

    def run(self, dataframe: DataFrame) -> Tuple[DataFrame, DataFrame, DataFrame]:
        new_dataset, empty_phone_numbers, ignored_records = self.parse_dataset(dataframe)
        return new_dataset, empty_phone_numbers, ignored_records
