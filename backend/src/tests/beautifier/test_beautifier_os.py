from mocks import MOCK_DATA

from src.core.beautifier.beautifier import PhoneNumbersBeautifier
from src.tests.beautifier.fixtures import *

beautifier = PhoneNumbersBeautifier(MOCK_DATA["config_os"], "os")


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


def test_check_if_region_is_disallowed(row_for_nonexistent_region):
    parsed_row = beautifier.parse_row(row_for_nonexistent_region)
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
    expected_result = 66

    assert result == expected_result


def test_get_federal_district(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    region = beautifier.get_refined_region(parsed_row)
    result = beautifier.get_federal_district(region)
    expected_result = "Уральский"

    assert result == expected_result


def test_get_federal_district_code(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    region = beautifier.get_refined_region(parsed_row)
    federal_district = beautifier.get_federal_district(region)
    result = beautifier.get_federal_district_code(federal_district)
    expected_result = 6

    assert result == expected_result


#
#
def test_get_filial_code(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    region = beautifier.get_refined_region(parsed_row)
    result = beautifier.get_filial_code(region)
    expected_result = 7

    assert result == expected_result


def test_get_operator(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    result = beautifier.get_operator(parsed_row)
    expected_result = 7

    assert result == expected_result


def test_make_log_row_for_OS(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    result = beautifier.make_log_row_for_missing_region_for_OS(parsed_row)
    expected_result = {
        "Number": "79001979228",
        "DisplayField2": "Свердловская обл.",
        "oper": 'ООО "ЕКАТЕРИНБУРГ-2000"',
        "reason": "Такого региона нет на вкладке 'Region-->OS_Region'",
    }

    assert result == expected_result


def test_make_tailored_row_for_OS(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    result = beautifier.make_tailored_row_for_OS(parsed_row)
    expected_result = {
        "Number": "79001979228",
        "ВнешнийID": "9001979228",
        "DisplayField1": "Уральский",
        "DisplayField2": "Свердловская область",
        "DisplayField3": 6,
        "filial": 7,
        "obl": 66,
        "CallIntervalBegin": "07:00:00",
        "CallIntervalEnd": "20:00:00",
        "oper": 7,
        "Mark": 66,
    }

    assert result == expected_result


def test_check_if_region_is_ignored_for_OS_for_usual_case(row_simple):
    parsed_row = beautifier.parse_row(row_simple)
    tailored_row = beautifier.make_tailored_row_for_OS(parsed_row)
    result = beautifier.check_if_region_is_ignored_for_OS(tailored_row)

    assert result == False


def test_check_if_region_is_ignored_for_OS_for_chukotka(row_for_chukotka):
    parsed_row = beautifier.parse_row(row_for_chukotka)
    tailored_row = beautifier.make_tailored_row_for_OS(parsed_row)
    result = beautifier.check_if_region_is_ignored_for_OS(tailored_row)

    assert result == True
