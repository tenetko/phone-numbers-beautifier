from src.core.tzb_checker.tzb_checker import TZBChecker
from src.tests.tzb_checker.fixtures import *


def test_check_source(
    check_list_dataframe, source_dataframe, expected_checked_source_dataframe, expected_completed_dataframe
):
    checker = TZBChecker(check_list_dataframe)
    checked_source_dataframe, completed_dataframe = checker.check_source(source_dataframe)

    assert checked_source_dataframe.equals(expected_checked_source_dataframe)
    assert completed_dataframe.equals(expected_completed_dataframe)
