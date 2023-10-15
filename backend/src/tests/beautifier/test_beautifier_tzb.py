from mocks import MOCK_DATA

from src.core.beautifier.beautifier import PhoneNumbersBeautifier
from src.tests.beautifier.fixtures import *

beautifier = PhoneNumbersBeautifier(MOCK_DATA["config_tzb"], "tzb")


def test_parse_row(row_simple):
    result = beautifier.parse_row(row_simple)
    expected_result = {
        "phone_number": "79001979228",
        "region": "Свердловская обл.",
        "operator": 'ООО "ЕКАТЕРИНБУРГ-2000"',
    }

    assert result == expected_result


def test_check_if_region_is_allowed(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    result = beautifier.check_if_region_is_allowed(parsed_row)
    expected_result = True

    assert result == expected_result


def test_check_if_region_is_disallowed(row_for_chukotka):
    parsed_row = beautifier.parse_row(row_for_chukotka)
    result = beautifier.check_if_region_is_allowed(parsed_row)
    expected_result = False

    assert result == expected_result


def test_validate_phone_number():
    num1 = "89001234567"
    num2 = "9008889911"

    result_1 = beautifier.try_to_validate_phone_number(num1)
    result_2 = beautifier.try_to_validate_phone_number(num2)

    expected_result_1 = "79001234567"
    expected_result_2 = "79008889911"

    assert result_1 == expected_result_1
    assert result_2 == expected_result_2


def test_check_if_phone_number_is_valid():
    num1 = "79001231231"
    num2 = "7900123123"
    num3 = "89001231231"
    num4 = "8900123123"
    num5 = "74950000000"
    num6 = "88622231231"
    num7 = "69001231231"
    num8 = "кукушкапока"
    num9 = "+79001231231"

    result_1 = beautifier.check_if_phone_number_is_valid(num1)
    result_2 = beautifier.check_if_phone_number_is_valid(num2)
    result_3 = beautifier.check_if_phone_number_is_valid(num3)
    result_4 = beautifier.check_if_phone_number_is_valid(num4)
    result_5 = beautifier.check_if_phone_number_is_valid(num5)
    result_6 = beautifier.check_if_phone_number_is_valid(num6)
    result_7 = beautifier.check_if_phone_number_is_valid(num7)
    result_8 = beautifier.check_if_phone_number_is_valid(num8)
    result_9 = beautifier.check_if_phone_number_is_valid(num9)

    assert result_1 == True
    assert result_2 == False
    assert result_3 == True
    assert result_4 == False
    assert result_5 == False
    assert result_6 == False
    assert result_7 == False
    assert result_8 == False
    assert result_9 == False


def test_get_external_id():
    result = beautifier.get_external_id("+79991234567")
    expected_result = "9991234567"

    assert result == expected_result


def test_get_refined_region(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    result = beautifier.get_refined_region(parsed_row)
    expected_result = "Свердловская область"

    assert result == expected_result


def test_get_region_code(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    region = beautifier.get_refined_region(parsed_row)
    result = beautifier.get_region_code(region)
    expected_result = 12

    assert result == expected_result


def test_get_operator(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    result = beautifier.get_operator(parsed_row)
    expected_result = "Мотив"

    assert result == expected_result


def test_get_operator_code(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    operator = beautifier.get_operator(parsed_row)
    result = beautifier.get_operator_code(operator)
    expected_result = 7

    assert result == expected_result


def test_get_time_difference(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    region = beautifier.get_refined_region(parsed_row)
    result = beautifier.get_time_difference(region)
    expected_result = "UTC +5"

    assert result == expected_result


def test_get_tzb_group(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    region = beautifier.get_refined_region(parsed_row)
    operator = beautifier.get_operator(parsed_row)
    result = beautifier.get_tzb_group(region, operator)
    expected_result = "Свердловская область_Мотив"

    assert result == expected_result


def test_get_tzb_mark(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    region = beautifier.get_refined_region(parsed_row)
    operator = beautifier.get_operator(parsed_row)
    operator_code = beautifier.get_operator_code(operator)
    region_code = beautifier.get_region_code(region)
    result = beautifier.get_tzb_mark(region_code, operator_code)
    expected_result = "12_7"

    assert result == expected_result


def test_make_log_row_for_TZB(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    result = beautifier.make_log_row_for_missing_region_for_TZB(parsed_row)
    expected_result = {
        "Number": "79001979228",
        "RegionName": "Свердловская обл.",
        "OperatorName": 'ООО "ЕКАТЕРИНБУРГ-2000"',
        "reason": "Такого региона нет на вкладке 'Region-->TZB_Reg_code'",
    }

    assert result == expected_result


def test_make_tailored_row_for_TZB(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    result = beautifier.make_tailored_row_for_TZB(parsed_row)
    expected_result = {
        "Number": "79001979228",
        "RegionName": "Свердловская область",
        "OperatorName": "Мотив",
        "TimeDifference": "UTC +5",
        "Region": 12,
        "Operator": 7,
        "CallIntervalBegin": "08:00:00",
        "CallIntervalEnd": "20:00:00",
        "Group": "Свердловская область_Мотив",
        "CHECK": "9001979228",
        "Mark": "12_7",
    }

    assert result == expected_result


def test_check_if_operator_is_allowed_for_TZB_for_yota_moscow(row_for_yota_moscow):
    parsed_row = beautifier.parse_row(row_for_yota_moscow)
    tailored_row = beautifier.make_tailored_row_for_TZB(parsed_row)
    result = beautifier.check_if_operator_is_allowed_for_TZB(tailored_row)
    expected_result = True

    assert result == expected_result


def test_check_if_operator_is_allowed_for_TZB_for_yota_krasnodarskiy_kray(row_for_yota_krasnodar_kray):
    parsed_row = beautifier.parse_row(row_for_yota_krasnodar_kray)
    tailored_row = beautifier.make_tailored_row_for_TZB(parsed_row)
    result = beautifier.check_if_operator_is_allowed_for_TZB(tailored_row)
    expected_result = False

    assert result == expected_result


def test_check_if_operator_is_other_for_TZB_for_yota_moscow(row_for_yota_moscow):
    parsed_row = beautifier.parse_row(row_for_yota_moscow)
    tailored_row = beautifier.make_tailored_row_for_TZB(parsed_row)
    result = beautifier.check_if_operator_is_other_for_TZB(tailored_row)
    expected_result = False

    assert result == expected_result


def test_check_if_operator_is_other_for_TZB_for_sim_telecom(row_for_sim_telecom):
    parsed_row = beautifier.parse_row(row_for_sim_telecom)
    tailored_row = beautifier.make_tailored_row_for_TZB(parsed_row)
    result = beautifier.check_if_operator_is_other_for_TZB(tailored_row)
    expected_result = True

    assert result == expected_result


def test_get_refined_quota_region():
    result = beautifier.get_refined_quota_region("Удмуртская Республика")
    expected_result = "Республика Удмуртская"

    assert result == expected_result
