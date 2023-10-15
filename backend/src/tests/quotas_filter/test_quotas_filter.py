import json
from collections import defaultdict

from src.core.beautifier.beautifier import PhoneNumbersBeautifier
from src.core.quotas_filter.quotas_filter import QuotasFilter
from src.tests.beautifier.mocks import MOCK_DATA as BEAUTIFIER_MOCK_DATA
from src.tests.quotas_filter.fixtures import *
from src.tests.quotas_filter.mocks import MOCK_DATA as QUOTAS_FILTER_MOCK_DATA

beautifier = PhoneNumbersBeautifier(BEAUTIFIER_MOCK_DATA["config_tzb"], "tzb")
quotas_filter = QuotasFilter(beautifier)


def test_check_if_raw_region_name_is_valid_for_khakassia(quota_row_for_khakassia):
    raw_region_and_quota_name = str(quota_row_for_khakassia["Общая статистика"])
    result = quotas_filter.check_if_raw_region_name_is_valid(raw_region_and_quota_name)
    expected_result = True

    assert result == expected_result


def test_check_if_raw_region_name_is_valid_for_other_row(other_row):
    raw_region_and_quota_name = str(other_row["Общая статистика"])
    result = quotas_filter.check_if_raw_region_name_is_valid(raw_region_and_quota_name)
    expected_result = False

    assert result == expected_result


def test_get_region_name(quota_row_for_khakassia):
    raw_region_and_quota_name = str(quota_row_for_khakassia["Общая статистика"])
    result = quotas_filter.get_region_name(raw_region_and_quota_name)
    expected_result = "Республика Хакасия"

    assert result == expected_result


def test_get_quota_name(quota_row_for_khakassia):
    raw_region_and_quota_name = str(quota_row_for_khakassia["Общая статистика"])
    result = quotas_filter.get_quota_name(raw_region_and_quota_name)
    expected_result = "Женский 16-20"

    assert result == expected_result


def test_get_quota_value_for_empty_quota(quota_row_for_khakassia_with_empty_quota):
    result = quotas_filter.get_quota_value(quota_row_for_khakassia_with_empty_quota)
    expected_result = ""

    assert result == expected_result


def test_get_quota_usage(quota_row_for_khakassia):
    result = quotas_filter.get_quota_usage(quota_row_for_khakassia)
    expected_result = 3

    assert result == expected_result


def test_get_quota_balance():
    result = quotas_filter.get_quota_balance(7, 3)
    expected_result = 4

    assert result == expected_result


def test_get_quota_balance_for_empty_quota():
    result = quotas_filter.get_quota_balance("", 3)
    expected_result = ""

    assert result == expected_result


def test_get_quota_gender_for_empty_quota_name():
    result = quotas_filter.get_quota_gender("")
    expected_result = ""

    assert result == expected_result


def test_get_quota_gender_for_beeline():
    result = quotas_filter.get_quota_gender("Билайн")
    expected_result = ""

    assert result == expected_result


def test_get_quota_gender_for_female():
    result = quotas_filter.get_quota_gender("Женский")
    expected_result = "Женский"

    assert result == expected_result


def test_get_quota_gender_for_male():
    result = quotas_filter.get_quota_gender("Мужской")
    expected_result = "Мужской"

    assert result == expected_result


def test_get_quota_age_for_empty():
    result = quotas_filter.get_quota_age("")
    expected_result = ("", "")

    assert result == expected_result


def test_get_quota_age_for_beeline():
    result = quotas_filter.get_quota_age("Билайн")
    expected_result = ("", "")

    assert result == expected_result


def test_get_quota_age_for_group_female_16_35():
    quota_name = "Группа Женский 16-20 + 21-35"
    result = quotas_filter.get_quota_age(quota_name)
    expected_result = (16, 35)

    assert result == expected_result


def test_get_quota_age_for_group_16_35():
    quota_name = "Группа 16-20 + 21-35"
    result = quotas_filter.get_quota_age(quota_name)
    expected_result = (16, 35)

    assert result == expected_result


def test_get_quota_age_for_female_16_20():
    quota_name = "Женский 16-20"
    result = quotas_filter.get_quota_age(quota_name)
    expected_result = (16, 20)

    assert result == expected_result


def test_is_group_quota_match_for_matching_row():
    row = {"Number": 79004749572, "Пол": "Женский", "Возраст": 18}
    quota = {"gender": "Женский", "age_from": 16, "age_to": 20, "balance": 10}
    result = quotas_filter.is_group_quota_match(row, quota)
    expected_result = True

    assert result == expected_result


def test_is_group_quota_match_for_nonmatching_row():
    row = {"Number": 79004749572, "Пол": "Мужской", "Возраст": 18}
    quota = {"gender": "Женский", "age_from": 16, "age_to": 20, "balance": 10}
    result = quotas_filter.is_group_quota_match(row, quota)
    expected_result = False

    assert result == expected_result


def test_is_group_quota_match_for_non_gender_row():
    row = {"Number": 79004749572, "Пол": "Мужской", "Возраст": 18}
    quota = {"gender": "", "age_from": 16, "age_to": 20, "balance": 10}
    result = quotas_filter.is_group_quota_match(row, quota)
    expected_result = True

    assert result == expected_result


def test_is_group_quota_match_for_non_gender_row_when_age_doesnt_match():
    row = {"Number": 79004749572, "Пол": "Мужской", "Возраст": 18}
    quota = {"gender": "", "age_from": 21, "age_to": 35, "balance": 10}
    result = quotas_filter.is_group_quota_match(row, quota)
    expected_result = False

    assert result == expected_result


def test_is_quota_balance_zero_for_nonzero_quota():
    quota = {"gender": "Женский", "age_from": 16, "age_to": 20, "balance": 10}
    result = quotas_filter.is_quota_balance_zero(quota)
    expected_result = False

    assert result == expected_result


def test_is_quota_balance_zero_for_zero_quota():
    quota = {"gender": "Женский", "age_from": 16, "age_to": 20, "balance": 0}
    result = quotas_filter.is_quota_balance_zero(quota)
    expected_result = True

    assert result == expected_result


def test_make_new_row_with_zero_quota_for_region():
    row = {"Number": 79004749572, "Пол": "Мужской", "Возраст": 18}
    region_quotas = {
        "Весь регион": {"gender": "", "age_from": "", "age_to": "", "balance": 0},
    }
    result = quotas_filter.make_new_row_with_quota(row, region_quotas)
    expected_result = {
        "Number": 79004749572,
        "Пол": "Мужской",
        "Возраст": 18,
        "IsCallable": False,
        "Quota": '"Весь регион": {"gender": "", "age_from": "", "age_to": "", "balance": 0}',
    }

    assert result == expected_result


def test_make_new_row_with_nonzero_quota_for_groups():
    row = {"Number": 79004749572, "Пол": "Мужской", "Возраст": 18, "OperatorName": "Билайн"}
    region_quotas = {
        "Весь регион": {"gender": "", "age_from": "", "age_to": "", "balance": 10},
        "Мужской 16-20": {"gender": "Мужской", "age_from": 16, "age_to": 20, "balance": 30},
        "Группа Мужской 16-20 + 21-35": {"gender": "Мужской", "age_from": 16, "age_to": 35, "balance": 16},
        "Группа 16-20 + 21-35": {"gender": "", "age_from": 16, "age_to": 35, "balance": 36},
        "Билайн": {"gender": "", "age_from": "", "age_to": "", "balance": 12},
    }
    result = quotas_filter.make_new_row_with_quota(row, region_quotas)
    expected_result = {
        "Number": 79004749572,
        "Пол": "Мужской",
        "Возраст": 18,
        "OperatorName": "Билайн",
        "IsCallable": True,
        "Quota": json.dumps(region_quotas, ensure_ascii=False),
    }

    assert result == expected_result


def test_make_new_row_with_zero_quota_for_groups():
    row = {"Number": 79004749572, "Пол": "Мужской", "Возраст": 18, "OperatorName": "Билайн"}
    region_quotas = {
        "Весь регион": {"gender": "", "age_from": "", "age_to": "", "balance": 10},
        "Мужской 16-20": {"gender": "Мужской", "age_from": 16, "age_to": 20, "balance": ""},
        "Группа Мужской 16-20 + 21-35": {"gender": "Мужской", "age_from": 16, "age_to": 35, "balance": 16},
        "Группа 16-20 + 21-35": {"gender": "", "age_from": 16, "age_to": 35, "balance": 36},
        "Билайн": {"gender": "", "age_from": "", "age_to": "", "balance": 0},
    }
    result = quotas_filter.make_new_row_with_quota(row, region_quotas)
    expected_result = {
        "Number": 79004749572,
        "Пол": "Мужской",
        "Возраст": 18,
        "OperatorName": "Билайн",
        "IsCallable": False,
        "Quota": json.dumps(region_quotas, ensure_ascii=False),
    }

    assert result == expected_result


def test_make_new_row_with_empty_string_quota_for_groups():
    row = {"Number": 79004749572, "Пол": "Мужской", "Возраст": 18, "OperatorName": "Билайн"}
    region_quotas = {
        "Весь регион": {"gender": "", "age_from": "", "age_to": "", "balance": 10},
        "Мужской 16-20": {"gender": "Мужской", "age_from": 16, "age_to": 20, "balance": ""},
        "Группа Мужской 16-20 + 21-35": {"gender": "Мужской", "age_from": 16, "age_to": 35, "balance": ""},
        "Группа 16-20 + 21-35": {"gender": "", "age_from": 16, "age_to": 35, "balance": ""},
        "Билайн": {"gender": "", "age_from": "", "age_to": "", "balance": 12},
    }
    result = quotas_filter.make_new_row_with_quota(row, region_quotas)
    expected_result = {
        "Number": 79004749572,
        "Пол": "Мужской",
        "Возраст": 18,
        "OperatorName": "Билайн",
        "IsCallable": True,
        "Quota": json.dumps(region_quotas, ensure_ascii=False),
    }

    assert result == expected_result


def test_make_quotas_dictionary(quotas_dataframe):
    result = quotas_filter.make_quotas_dictionary(quotas_dataframe)
    expected_result = defaultdict(dict, QUOTAS_FILTER_MOCK_DATA["quotas_config"])

    assert result == expected_result
