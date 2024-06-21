import json
import re
from collections import defaultdict
from typing import Dict, Tuple

import pandas as pd
from pandas import DataFrame, Series

from src.core.beautifier.beautifier import PhoneNumbersBeautifier


class QuotasParser:
    REGION_TYPES = ["Республика", "республика", "область", "край", "АО"]
    FEDERAL_CITY_NAMES = ["Москва", "Санкт-Петербург"]

    def __init__(self, beautifier: PhoneNumbersBeautifier) -> None:
        self.beautifier = beautifier

    def make_quotas_dictionary(self, dataframe_with_quotas: DataFrame) -> Dict:
        quotas = defaultdict(dict)

        for _, row in dataframe_with_quotas.iterrows():
            raw_region_and_quota_name = str(row["Общая статистика"])

            if "Реклама" in raw_region_and_quota_name:
                break

            if not self.check_if_raw_region_name_is_valid(raw_region_and_quota_name):
                continue

            region_name = self.get_region_name(raw_region_and_quota_name)
            quota_name = self.get_quota_name(raw_region_and_quota_name)
            quota_value = self.get_quota_value(row)
            quota_usage = self.get_quota_usage(row)
            quota_age_from, quota_age_to = self.get_quota_age(quota_name)

            quotas[region_name][quota_name] = {
                "gender": self.get_quota_gender(quota_name),
                "age_from": quota_age_from,
                "age_to": quota_age_to,
                "balance": self.get_quota_balance(quota_value, quota_usage),
            }

        return quotas

    def check_if_raw_region_name_is_valid(self, raw_region_name: str) -> bool:
        if "РЕКРУТ" in raw_region_name:
            return False

        if not any(region_type in raw_region_name for region_type in self.REGION_TYPES):
            return False

        return True

    def get_region_name(self, raw_region_name: str) -> str:
        if any(fed_city_name in raw_region_name for fed_city_name in self.FEDERAL_CITY_NAMES):
            # "Москва / Московская область" --> "Москва и Московская область"
            # "Санкт-Петербург/Ленинградская область" --> "Санкт-Петербург и Ленинградская область"
            splitted_string = raw_region_name.split("/")
            city = splitted_string[0]
            region = splitted_string[1].split(">")[0].strip()
            region_name = f"{city} и {region}"

        elif "/" not in raw_region_name:
            region_name = raw_region_name.split(">")[0].strip()
        else:
            # "Абакан/Республика Хакасия" --> "Республика Хакасия"
            splitted_string = raw_region_name.split("/")
            region_name = splitted_string[1].split(">")[0].strip()

        region_name = self.beautifier.get_refined_quota_region(region_name)

        return region_name

    @staticmethod
    def get_quota_name(raw_quota_name) -> str:
        # "Абакан/Республика Хакасия > Женский 16-20" --> "Женский 16-20"
        if ">" not in raw_quota_name:
            return "Весь регион"

        splitted_string = raw_quota_name.split(">")

        # We had to hardcode that because we cannot get that changed in any other way
        if splitted_string[1].strip() == "Tele2":
            return "Теле-2"

        if splitted_string[1].strip() == "Yota (Йота)":
            return "Йота"

        return splitted_string[1].strip()

    @staticmethod
    def get_quota_value(row: Series) -> int | str:
        quota_value = row["Unnamed: 1"]
        if pd.isna(quota_value):
            return ""

        return int(quota_value)

    @staticmethod
    def get_quota_usage(row: Series) -> int:
        return int(row["Unnamed: 2"])

    @staticmethod
    def get_quota_balance(quota_value: int, quota_usage: int) -> int | str:
        if quota_value == "":
            return ""

        quota_balance = quota_value - quota_usage
        if quota_balance < 1:
            return 0

        return quota_balance

    @staticmethod
    def get_quota_gender(quota_name: str) -> str:
        if len(quota_name) == 0:
            return ""

        if "Женский" in quota_name:
            return "Женский"

        if "Мужской" in quota_name:
            return "Мужской"

        return ""

    @staticmethod
    def get_quota_age(quota_name: str) -> Tuple[int, int] | Tuple[str, str]:
        if "-" not in quota_name or quota_name == "Теле-2":
            # Билайн, Теле-2
            return "", ""

        if "+" in quota_name:
            # Группа Женский 16-20 + 21-35
            regex = re.compile(
                r"Группа (?P<gender>[а-яА-Я]*)\s?(?P<first_range_from>\d{1,2})-(?P<first_range_to>\d{1,2}) \+ "
                r"(?P<second_range_from>\d{1,2})-(?P<second_range_to>\d{1,2})"
            )
            result = regex.match(quota_name)
            return int(result["first_range_from"]), int(result["second_range_to"])
        else:
            # Женский 16-20
            ages = quota_name.split(" ")[1].split("-")
            return int(ages[0]), int(ages[1])
