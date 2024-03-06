import json
from typing import Dict, Tuple

from loguru import logger
from pandas import DataFrame

from src.utils.logging.logging import Sink


class GenderAgeExtender:
    def __init__(self):
        self.logs = Sink()
        logger.add(sink=self.logs, serialize=True)

    def make_extended_dataframe(self, dataframe_to_extend: DataFrame, dataframe_with_details: DataFrame) -> DataFrame:
        extended_dataset = []
        details_dict = self.make_details_dict(dataframe_with_details)

        for _, row in dataframe_to_extend.iterrows():
            row_dict = json.loads(row.to_json())
            phone_number = row["num"]

            try:
                details = details_dict[str(phone_number)]
            except KeyError:
                message = (
                    f"The source file does not have a phone number {phone_number} within specified date ranges. "
                    f"Try setting wider date ranges"
                )
                logger.exception(message)
                raise KeyError

            try:
                row_dict["Пол"] = details["gender"]
            except KeyError:
                logger.exception(f"The 'Пол' value is empty for phone {phone_number}")
                raise KeyError

            try:
                row_dict["Возраст"] = details["age"]
            except KeyError:
                logger.exception(f"The 'Возраст' value is empty for phone {phone_number}")
                raise KeyError

            try:
                row_dict["iSayMail"] = details["email"]
            except KeyError:
                logger.exception(f"The 'iSayMail' value is empty for phone {phone_number}")
                raise KeyError

            try:
                row_dict["REGION"] = details["adjusted_region"]
            except KeyError:
                logger.exception(f"The 'REGION' value is empty for phone {phone_number}")
                raise KeyError

            try:
                row_dict["Reward"] = details["reward"]
            except KeyError:
                logger.exception(f"The 'Reward' value is empty for phone {phone_number}")
                raise KeyError

            try:
                row_dict["Source"] = details["Source"]
            except KeyError:
                logger.exception(f"The 'Source' value is empty for phone {phone_number}")
                raise KeyError

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
                "Source": row["Source"],
            }

        return result
