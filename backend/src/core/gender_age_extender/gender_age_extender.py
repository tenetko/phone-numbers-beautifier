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
            details = details_dict[row["Number"]]

            row_dict["Пол"] = details["gender"]
            row_dict["Возраст"] = details["age"]
            row_dict["Email"] = details["email"]

            extended_dataset.append(row_dict)

        return DataFrame(extended_dataset)

    def make_details_dict(self, dataframe_with_details: DataFrame) -> Dict[str, Dict[str, str]]:
        result = {}

        for _, row in dataframe_with_details.iterrows():
            result[str(row["Номер телефона"])] = {
                "gender": row["Пол"],
                "age": row["Возраст"],
                "email": row["Email"],
            }

        return result
