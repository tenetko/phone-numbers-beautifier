from pandas import DataFrame
from pytest import fixture

from src.tests.tzb_filter.mocks import MOCK_DATA


@fixture
def check_list_dataframe() -> DataFrame:
    return DataFrame(MOCK_DATA["check_list"])


@fixture
def source_dataframe() -> DataFrame:
    return DataFrame(MOCK_DATA["source"])


@fixture
def macros_dataframe() -> DataFrame:
    return DataFrame(MOCK_DATA["macros"])


@fixture
def expected_checked_source_dataframe() -> DataFrame:
    return DataFrame(MOCK_DATA["expected_checked_source"])


@fixture
def expected_completed_dataframe() -> DataFrame:
    return DataFrame(MOCK_DATA["completed"])


@fixture
def expected_filtered_by_macros_source_dataframe() -> DataFrame:
    return DataFrame(MOCK_DATA["expected_filtered_by_macros_source"])
