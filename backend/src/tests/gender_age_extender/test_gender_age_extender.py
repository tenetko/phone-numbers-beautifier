from src.core.gender_age_extender.gender_age_extender import GenderAgeExtender
from src.tests.gender_age_extender.fixtures import *

extender = GenderAgeExtender()


def test_make_details_dict(base_details_dataframe):
    result = extender.make_details_dict(base_details_dataframe)
    expected_result = {
        "79991234567": {
            "gender": "Женский",
            "age": "27",
            "email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
        }
    }

    assert result == expected_result


def test_make_extended_dataframe(base_dataframe, base_details_dataframe):
    result = extender.make_extended_dataframe(base_dataframe, base_details_dataframe)
    expected_result = DataFrame(
        [
            {
                "Number": "79991234567",
                "RegionName": "Красноярский край",
                "OperatorName": "Мегафон",
                "TimeDifference": "UTC +7",
                "Region": "23",
                "Operator": "3",
                "CallIntervalBegin": "06:00:00",
                "CallIntervalEnd": "18:00:00",
                "Group": "Красноярский край_Мегафон",
                "CHECK": "9237847777",
                "Mark": "23_3",
                "Пол": "Женский",
                "Возраст": "27",
                "Email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            }
        ]
    )

    assert result.equals(expected_result)
