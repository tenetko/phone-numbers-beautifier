import json
from collections import defaultdict

from src.core.beautifier.beautifier import PhoneNumbersBeautifier
from src.core.quotas_parser.quotas_parser import QuotasParser
from src.tests.beautifier.mocks import MOCK_DATA as BEAUTIFIER_MOCK_DATA
from src.tests.quotas_parser.fixtures import *
from src.tests.quotas_parser.mocks import MOCK_DATA as QUOTAS_PARSER_MOCK_DATA

beautifier = PhoneNumbersBeautifier(BEAUTIFIER_MOCK_DATA["config_tzb"], "tzb")
quotas_parser = QuotasParser(beautifier)


def test_check_if_raw_region_name_is_valid_for_khakassia(quota_row_for_khakassia):
    raw_region_and_quota_name = str(quota_row_for_khakassia["Общая статистика"])
    result = quotas_parser.check_if_raw_region_name_is_valid(raw_region_and_quota_name)
    expected_result = True

    assert result == expected_result


def test_check_if_raw_region_name_is_valid_for_other_row(other_row):
    raw_region_and_quota_name = str(other_row["Общая статистика"])
    result = quotas_parser.check_if_raw_region_name_is_valid(raw_region_and_quota_name)
    expected_result = False

    assert result == expected_result


def test_get_region_name(quota_row_for_khakassia):
    raw_region_and_quota_name = str(quota_row_for_khakassia["Общая статистика"])
    result = quotas_parser.get_region_name(raw_region_and_quota_name)
    expected_result = "Республика Хакасия"

    assert result == expected_result


def test_get_quota_name(quota_row_for_khakassia):
    raw_region_and_quota_name = str(quota_row_for_khakassia["Общая статистика"])
    result = quotas_parser.get_quota_name(raw_region_and_quota_name)
    expected_result = "Женский 16-20"

    assert result == expected_result


def test_get_quota_value_for_empty_quota(quota_row_for_khakassia_with_empty_quota):
    result = quotas_parser.get_quota_value(quota_row_for_khakassia_with_empty_quota)
    expected_result = ""

    assert result == expected_result


def test_get_quota_usage(quota_row_for_khakassia):
    result = quotas_parser.get_quota_usage(quota_row_for_khakassia)
    expected_result = 3

    assert result == expected_result


def test_get_quota_balance():
    result = quotas_parser.get_quota_balance(7, 3)
    expected_result = 4

    assert result == expected_result


def test_get_quota_balance_for_empty_quota():
    result = quotas_parser.get_quota_balance("", 3)
    expected_result = ""

    assert result == expected_result


def test_get_quota_gender_for_empty_quota_name():
    result = quotas_parser.get_quota_gender("")
    expected_result = ""

    assert result == expected_result


def test_get_quota_gender_for_beeline():
    result = quotas_parser.get_quota_gender("Билайн")
    expected_result = ""

    assert result == expected_result


def test_get_quota_gender_for_female():
    result = quotas_parser.get_quota_gender("Женский")
    expected_result = "Женский"

    assert result == expected_result


def test_get_quota_gender_for_male():
    result = quotas_parser.get_quota_gender("Мужской")
    expected_result = "Мужской"

    assert result == expected_result


def test_get_quota_age_for_empty():
    result = quotas_parser.get_quota_age("")
    expected_result = ("", "")

    assert result == expected_result


def test_get_quota_age_for_beeline():
    result = quotas_parser.get_quota_age("Билайн")
    expected_result = ("", "")

    assert result == expected_result


def test_get_quota_age_for_group_female_16_35():
    quota_name = "Группа Женский 16-20 + 21-35"
    result = quotas_parser.get_quota_age(quota_name)
    expected_result = (16, 35)

    assert result == expected_result


def test_get_quota_age_for_group_16_35():
    quota_name = "Группа 16-20 + 21-35"
    result = quotas_parser.get_quota_age(quota_name)
    expected_result = (16, 35)

    assert result == expected_result


def test_get_quota_age_for_female_16_20():
    quota_name = "Женский 16-20"
    result = quotas_parser.get_quota_age(quota_name)
    expected_result = (16, 20)

    assert result == expected_result


def test_make_quotas_dictionary(quotas_dataframe):
    result = quotas_parser.make_quotas_dictionary(quotas_dataframe)
    expected_result = defaultdict(dict, QUOTAS_PARSER_MOCK_DATA["quotas_config"])

    assert result == expected_result
