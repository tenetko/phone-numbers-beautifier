from pandas import DataFrame
from pytest import fixture


@fixture
def base_dataframe() -> DataFrame:
    return DataFrame(
        [
            {
                "num": "79991234567",
                "REGION": "Красноярский край",
                "OPERATOR": "Мегафон",
            }
        ]
    )


@fixture
def base_details_dataframe() -> DataFrame:
    return DataFrame(
        [
            {
                "Статус": "Повторный",
                "ID": "01805ce5-111e-49a8-80b7-77c67bb020c4",
                "Имя": "Кристина",
                "Номер телефона": "79991234567",
                "Пол": "Женский",
                "Возраст": "27",
                "Почтовый индекс": "400062",
                "Регион": "Волгоградская область",
                "Город": "Волгоград",
                "Дата и время": "2023-09-20 00:56",
                "Дата": "2023-09-20",
                "Email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
                "Обещанная награда": "150",
            }
        ]
    )
