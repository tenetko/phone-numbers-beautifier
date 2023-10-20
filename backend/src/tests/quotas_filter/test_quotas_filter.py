import json

import pandas as pd

from src.core.beautifier.beautifier import PhoneNumbersBeautifier
from src.core.quotas_filter.quotas_filter import QuotasFilter
from src.core.quotas_parser.quotas_parser import QuotasParser
from src.tests.beautifier.mocks import MOCK_DATA as BEAUTIFIER_MOCK_DATA
from src.tests.quotas_parser.fixtures import quotas_dataframe

quotas_filter = QuotasFilter()
beautifier = PhoneNumbersBeautifier(BEAUTIFIER_MOCK_DATA["config_tzb"], "tzb")
quotas_parser = QuotasParser(beautifier)


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


def test_filter_phone_numbers(quotas_dataframe):
    quotas_dict = quotas_parser.make_quotas_dictionary(quotas_dataframe)
    dataframe = pd.DataFrame(
        [{"RegionName": "Республика Хакасия", "OperatorName": "МТС", "Пол": "Мужской", "Возраст": 36}]
    )
    result = quotas_filter.filter_phone_numbers(dataframe, quotas_dict)

    expected_result_1 = pd.DataFrame(
        [
            {
                "RegionName": "Республика Хакасия",
                "OperatorName": "МТС",
                "Пол": "Мужской",
                "Возраст": 36,
                "IsCallable": True,
                "Quota": json.dumps(
                    {
                        "Весь регион": {"gender": "", "age_from": "", "age_to": "", "balance": 34},
                        "Мужской 36-45": {"gender": "Мужской", "age_from": 36, "age_to": 45, "balance": ""},
                        "Группа Мужской 36-45 + 46-55": {
                            "gender": "Мужской",
                            "age_from": 36,
                            "age_to": 55,
                            "balance": "",
                        },
                        "Группа 36-45 + 46-55": {"gender": "", "age_from": 36, "age_to": 55, "balance": ""},
                        "МТС": {"gender": "", "age_from": "", "age_to": "", "balance": 25},
                    },
                    ensure_ascii=False,
                ),
            }
        ]
    )
    expected_result_2 = pd.DataFrame()

    assert result[0].equals(expected_result_1)
    assert result[1].equals(expected_result_2)


def test_filter_reminders(quotas_dataframe):
    quotas_dict = quotas_parser.make_quotas_dictionary(quotas_dataframe)
    dataframe = pd.DataFrame(
        [
            {
                "RegionName": "Республика Хакасия",
                "OperatorName": "МТС",
                "Group": "191_13_Республика Хакасия_МТС_М3645",
            }
        ]
    )
    result = quotas_filter.filter_reminders(dataframe, quotas_dict)

    expected_result_1 = pd.DataFrame(
        [
            {
                "RegionName": "Республика Хакасия",
                "OperatorName": "МТС",
                "Group": "191_13_Республика Хакасия_МТС_М3645",
                "Пол": "Мужской",
                "Возраст": 36,
                "IsCallable": True,
                "Quota": json.dumps(
                    {
                        "Весь регион": {"gender": "", "age_from": "", "age_to": "", "balance": 34},
                        "Мужской 36-45": {"gender": "Мужской", "age_from": 36, "age_to": 45, "balance": ""},
                        "Группа Мужской 36-45 + 46-55": {
                            "gender": "Мужской",
                            "age_from": 36,
                            "age_to": 55,
                            "balance": "",
                        },
                        "Группа 36-45 + 46-55": {"gender": "", "age_from": 36, "age_to": 55, "balance": ""},
                        "МТС": {"gender": "", "age_from": "", "age_to": "", "balance": 25},
                    },
                    ensure_ascii=False,
                ),
            }
        ]
    )
    expected_result_2 = pd.DataFrame()

    assert result[0].equals(expected_result_1)
    assert result[1].equals(expected_result_2)


def test_get_age_and_gender_from_reminder():
    row = {
        "Group": "191_13_Республика Хакасия_МТС_М3645",
    }
    result = quotas_filter.get_age_and_gender_from_reminder(row)
    expected_result = ("Мужской", 36)

    assert result == expected_result
