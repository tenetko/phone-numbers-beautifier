from src.core.tzb_filter.tzb_filter import TZBFilter
from src.tests.tzb_filter.fixtures import *


def test_filter_with_checklist(
    check_list_dataframe,
    source_dataframe,
    macros_dataframe,
    expected_checked_source_dataframe,
    expected_completed_dataframe,
):
    checker = TZBFilter(check_list_dataframe, macros_dataframe)
    checked_source_dataframe, completed_dataframe = checker.filter_with_checklist(source_dataframe)

    assert checked_source_dataframe.equals(expected_checked_source_dataframe)
    assert completed_dataframe.equals(expected_completed_dataframe)


def test_filter_with_macros(
    check_list_dataframe, macros_dataframe, source_dataframe, expected_filtered_by_macros_source_dataframe
):
    checker = TZBFilter(check_list_dataframe, macros_dataframe)
    checked_source_dataframe, completed_dataframe = checker.filter_with_checklist(source_dataframe)
    filtered_by_macros_source_dataframe = checker.filter_with_macros(checked_source_dataframe)

    assert filtered_by_macros_source_dataframe.equals(expected_filtered_by_macros_source_dataframe)
