from pandas import DataFrame, Series
from pytest import fixture

from src.tests.tzb_template_parser.mocks import MOCK_DATA

@fixture
def source_dataframe() -> DataFrame:
    return DataFrame(MOCK_DATA["source"])
