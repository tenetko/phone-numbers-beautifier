from pandas import Series
from pytest import fixture


@fixture
def row_simple() -> Series:
    return Series(
        data={
            "Номер телефона": 79001979228,
            "IdRegion": 83,
            "IdOper": 28,
            "Регион": "Свердловская обл.",
            "Оператор сотовой связи": 'ООО "ЕКАТЕРИНБУРГ-2000"',
            "Пол": "Ж",
            "Возраст": 30,
            "Email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Обещанная награда": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_simple_for_os() -> Series:
    return Series(
        data={
            "num": 79001979228,
            "IdRegion": 83,
            "IdOper": 28,
            "REGION": "Свердловская обл.",
            "OPERATOR": 'ООО "ЕКАТЕРИНБУРГ-2000"',
            "Пол": "Ж",
            "Возраст": 30,
            "Email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Обещанная награда": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_simple_source_two() -> Series:
    return Series(
        data={
            "Номер телефона": 79001979228,
            "IdRegion": 83,
            "IdOper": 28,
            "Регион": "Свердловская обл.",
            "Оператор сотовой связи": 'ООО "ЕКАТЕРИНБУРГ-2000"',
            "Пол": "Ж",
            "Возраст": 30,
            "Email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Обещанная награда": 150,
            "Source": "source_two",
        }
    )


@fixture
def row_for_nonexistent_region() -> Series:
    return Series(
        data={
            "Номер телефона": 79001979228,
            "IdRegion": 83,
            "IdOper": 28,
            "Регион": "Волчий край",
            "Оператор сотовой связи": 'ООО "ЕКАТЕРИНБУРГ-2000"',
            "Пол": "Ж",
            "Возраст": 30,
            "Email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Обещанная награда": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_for_nonexistent_region_for_os() -> Series:
    return Series(
        data={
            "num": 79001979228,
            "IdRegion": 83,
            "IdOper": 28,
            "REGION": "Волчий край",
            "OPERATOR": 'ООО "ЕКАТЕРИНБУРГ-2000"',
            "Пол": "Ж",
            "Возраст": 30,
            "Email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Обещанная награда": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_for_chukotka() -> Series:
    return Series(
        data={
            "Номер телефона": 79001979228,
            "IdRegion": 104,
            "IdOper": 78,
            "Регион": "Чукотский АО",
            "Оператор сотовой связи": 'ПАО "Вымпел-Коммуникации"',
            "Пол": "Ж",
            "Возраст": 30,
            "Email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Обещанная награда": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_for_chukotka_for_os() -> Series:
    return Series(
        data={
            "num": 79001979228,
            "IdRegion": 104,
            "IdOper": 78,
            "REGION": "Чукотский АО",
            "OPERATOR": 'ПАО "Вымпел-Коммуникации"',
            "Пол": "Ж",
            "Возраст": 30,
            "Email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Обещанная награда": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_for_motiv() -> Series:
    return Series(
        data={
            "Номер телефона": 79011234567,
            "IdRegion": 83,
            "IdOper": 28,
            "Регион": "Курганская обл.",
            "Оператор сотовой связи": 'ООО "ЕКАТЕРИНБУРГ-2000"',
            "Пол": "Ж",
            "Возраст": 30,
            "Email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Обещанная награда": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_for_yota_moscow() -> Series:
    return Series(
        data={
            "Номер телефона": 79029876543,
            "IdRegion": 83,
            "IdOper": 28,
            "Регион": "г. Москва * Московская область",
            "Оператор сотовой связи": 'ООО "Скартел"',
            "Пол": "Ж",
            "Возраст": 30,
            "Email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Обещанная награда": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_for_yota_krasnodar_kray() -> Series:
    return Series(
        data={
            "Номер телефона": 79029876543,
            "IdRegion": 83,
            "IdOper": 28,
            "Регион": "Краснодарский край",
            "Оператор сотовой связи": 'ООО "Скартел"',
            "Пол": "Ж",
            "Возраст": 30,
            "Email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Обещанная награда": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_for_sim_telecom() -> Series:
    return Series(
        data={
            "Номер телефона": 79029876543,
            "IdRegion": 83,
            "IdOper": 28,
            "Регион": "Краснодарский край",
            "Оператор сотовой связи": 'ООО "СИМ ТЕЛЕКОМ"',
            "Пол": "Ж",
            "Возраст": 30,
            "Email": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Обещанная награда": 150,
            "Source": "source_one",
        }
    )
