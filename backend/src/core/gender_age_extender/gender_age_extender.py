import json
from typing import Dict, List

import pandas as pd
from pandas import DataFrame


class GenderAgeExtender:
    def make_extended_dataframe(self, dataframe_to_extend: DataFrame, dataframe_with_details: DataFrame) -> DataFrame:
        extended_dataset = []
        details_dict = self.make_details_dict(dataframe_with_details)

        for _, row in dataframe_to_extend.iterrows():
            row_dict = json.loads(row.to_json())
            details = details_dict[str(row["num"])]

            row_dict["Пол"] = details["gender"]
            row_dict["Возраст"] = details["age"]
            row_dict["iSayMail"] = details["email"]
            row_dict["REGION"] = details["adjusted_region"]
            row_dict["Reward"] = details["reward"]

            extended_dataset.append(row_dict)

        return DataFrame(extended_dataset)

    def make_details_dict(self, dataframe_with_details: DataFrame) -> Dict[str, Dict[str, str]]:
        result = {}

        for _, row in dataframe_with_details.iterrows():
            result[str(row["Номер телефона"])] = {
                "gender": row["Пол"],
                "age": row["Возраст"],
                "email": row["Email"],
                "adjusted_region": row["Регион"],
                "reward": row["Обещанная награда"],
            }

        return result
