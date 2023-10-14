from pandas import DataFrame
from pytest import fixture


@fixture
def base_dataframe() -> DataFrame:
    return DataFrame(
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
