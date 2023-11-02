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
            "adjusted_region": "Волгоградская область",
        }
    }

    assert result == expected_result


def test_make_extended_dataframe(base_dataframe, base_details_dataframe):
    result = extender.make_extended_dataframe(base_dataframe, base_details_dataframe)
    expected_result = DataFrame(
        [
            {
                "num": "79991234567",
                "REGION": "Волгоградская область",
                "OPERATOR": "Мегафон",
                "Пол": "Женский",
                "Возраст": "27",
                "Email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            }
        ]
    )

    assert result.equals(expected_result)
