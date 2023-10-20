from pandas import DataFrame, Series
from pytest import fixture

from src.tests.quotas_parser.mocks import MOCK_DATA


@fixture
def quota_row_for_khakassia() -> Series:
    return Series(
        {
            "Общая статистика": "Абакан/Республика Хакасия > Женский 16-20",
            "Unnamed: 1": 7,
            "Unnamed: 2": 3,
        }
    )


@fixture
def quota_row_for_khakassia_with_empty_quota() -> Series:
    return Series(
        {
            "Общая статистика": "Абакан/Республика Хакасия > Женский 16-20",
            "Unnamed: 1": None,
            "Unnamed: 2": 3,
        }
    )


@fixture
def other_row():
    return Series(
        {
            "Общая статистика": "Первое интервью",
            "Unnamed: 1": "26.08.2023 10:03:11",
            "Unnamed: 2": None,
        }
    )


@fixture
def quotas_dataframe() -> DataFrame:
    return DataFrame(MOCK_DATA["quotas"])
