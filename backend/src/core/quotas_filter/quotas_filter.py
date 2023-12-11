import json
from typing import Tuple

import pandas as pd
from pandas import DataFrame


class QuotasFilter:
    def filter_phone_numbers(self, phone_numbers: DataFrame, quotas: dict) -> Tuple[DataFrame, DataFrame]:
        rows_with_quotas = []
        rows_with_errors = []

        for _, row in phone_numbers.iterrows():
            new_row = dict(row)
            region_quotas = quotas[row["RegionName"]]

            try:
                row_with_quotas = self.make_new_row_with_quota(new_row, region_quotas)
                rows_with_quotas.append(row_with_quotas)
            except KeyError as e:
                row_json = dict(row)
                row_json["reason"] = f"Нe найдена квота '{e}'"
                rows_with_errors.append(row_json)

        return pd.DataFrame(rows_with_quotas), pd.DataFrame(rows_with_errors)

    def filter_reminders(self, phone_numbers: DataFrame, quotas: dict) -> Tuple[DataFrame, DataFrame]:
        rows_with_quotas = []
        rows_with_errors = []

        for _, row in phone_numbers.iterrows():
            new_row = dict(row)
            if pd.isna(row["Group"]):
                continue

            new_row["Пол"], new_row["Возраст"] = self.get_age_and_gender_from_reminder(new_row)

            region_name = row["RegionName"]
            # 'Хабаровский край' is the only region name that differs between 'край' and 'Край' in different sources.
            # We have to make this condition to keep regions consistent according to our internal standard.
            region_quotas = {}
            if region_name == "Хабаровский край":
                region_quotas == quotas["Хабаровский Край"]
            else:
                region_quotas = quotas[region_name]

            try:
                row_with_quotas = self.make_new_row_with_quota(new_row, region_quotas)
                rows_with_quotas.append(row_with_quotas)
            except KeyError as e:
                row_json = dict(row)
                row_json["reason"] = f"Нe найдена квота '{e}'"
                rows_with_errors.append(row_json)

        return pd.DataFrame(rows_with_quotas), pd.DataFrame(rows_with_errors)

    def make_new_row_with_quota(self, new_row: dict, region_quotas: dict) -> dict:
        region_quota = region_quotas["Весь регион"]
        if region_quota["balance"] <= 0:
            new_row["IsCallable"] = False
            new_row["Quota"] = f'"Весь регион": {json.dumps(region_quota, ensure_ascii=False)}'

            return new_row

        matching_quotas = dict()
        matching_quotas["Весь регион"] = region_quotas["Весь регион"]
        for quota_name in region_quotas:
            quota = region_quotas[quota_name]
            if self.is_group_quota_match(new_row, quota):
                matching_quotas[quota_name] = quota

        operator = new_row["OperatorName"]
        matching_quotas[operator] = region_quotas[operator]

        if all(
            matching_quotas[quota_name]["balance"] == "" or matching_quotas[quota_name]["balance"] > 0
            for quota_name in matching_quotas
        ):
            new_row["IsCallable"] = True
            new_row["Quota"] = f"{json.dumps(matching_quotas, ensure_ascii=False)}"
        else:
            new_row["IsCallable"] = False
            new_row["Quota"] = f"{json.dumps(matching_quotas, ensure_ascii=False)}"

        return new_row

    @staticmethod
    def is_group_quota_match(new_row: dict, quota: dict) -> bool:
        if (
            new_row["Пол"] == quota["gender"]
            or quota["gender"] == ""
            and isinstance(quota["age_from"], int)
            and isinstance(quota["age_to"], int)
        ) and quota["age_from"] <= new_row["Возраст"] <= quota["age_to"]:
            return True

        return False

    @staticmethod
    def is_quota_balance_zero(quota: dict) -> bool:
        if quota["balance"] == 0:
            return True

        return False

    def get_age_and_gender_from_reminder(self, row: dict) -> Tuple[str, str]:
        # "513_23_Тюменская область_Мегафон_Ж3645" --> ("Ж", "36")
        group = row["Group"][-5:]  # Ж3645
        age = int(group[1:3])
        gender = group[:1]
        if gender == "М":
            gender = "Мужской"
        elif gender == "Ж":
            gender = "Женский"
        else:
            raise ValueError("Gender is neither М nor Ж")

        return gender, age
