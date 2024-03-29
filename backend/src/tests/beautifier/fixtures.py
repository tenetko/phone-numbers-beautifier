from pandas import Series
from pytest import fixture


@fixture
def row_simple() -> Series:
    return Series(
        data={
            "num": 79001979228,
            "IdRegion": 83,
            "IdOper": 28,
            "REGION": "Свердловская обл.",
            "OPERATOR": 'ООО "ЕКАТЕРИНБУРГ-2000"',
            "Пол": "Ж",
            "Возраст": 30,
            "iSayMail": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Reward": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_simple_source_two() -> Series:
    return Series(
        data={
            "num": 79001979228,
            "IdRegion": 83,
            "IdOper": 28,
            "REGION": "Свердловская обл.",
            "OPERATOR": 'ООО "ЕКАТЕРИНБУРГ-2000"',
            "Пол": "Ж",
            "Возраст": 30,
            "iSayMail": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Reward": 150,
            "Source": "source_two",
        }
    )


@fixture
def row_for_nonexistent_region() -> Series:
    return Series(
        data={
            "num": 79001979228,
            "IdRegion": 83,
            "IdOper": 28,
            "REGION": "Волчий край",
            "OPERATOR": 'ООО "ЕКАТЕРИНБУРГ-2000"',
            "Пол": "Ж",
            "Возраст": 30,
            "iSayMail": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Reward": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_for_chukotka() -> Series:
    return Series(
        data={
            "num": 79001979228,
            "IdRegion": 104,
            "IdOper": 78,
            "REGION": "Чукотский АО",
            "OPERATOR": 'ПАО "Вымпел-Коммуникации"',
            "Пол": "Ж",
            "Возраст": 30,
            "iSayMail": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Reward": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_for_motiv() -> Series:
    return Series(
        data={
            "num": 79011234567,
            "IdRegion": 83,
            "IdOper": 28,
            "REGION": "Курганская обл.",
            "OPERATOR": 'ООО "ЕКАТЕРИНБУРГ-2000"',
            "Пол": "Ж",
            "Возраст": 30,
            "iSayMail": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Reward": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_for_yota_moscow() -> Series:
    return Series(
        data={
            "num": 79029876543,
            "IdRegion": 83,
            "IdOper": 28,
            "REGION": "г. Москва * Московская область",
            "OPERATOR": 'ООО "Скартел"',
            "Пол": "Ж",
            "Возраст": 30,
            "iSayMail": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Reward": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_for_yota_krasnodar_kray() -> Series:
    return Series(
        data={
            "num": 79029876543,
            "IdRegion": 83,
            "IdOper": 28,
            "REGION": "Краснодарский край",
            "OPERATOR": 'ООО "Скартел"',
            "Пол": "Ж",
            "Возраст": 30,
            "iSayMail": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Reward": 150,
            "Source": "source_one",
        }
    )


@fixture
def row_for_sim_telecom() -> Series:
    return Series(
        data={
            "num": 79029876543,
            "IdRegion": 83,
            "IdOper": 28,
            "REGION": "Краснодарский край",
            "OPERATOR": 'ООО "СИМ ТЕЛЕКОМ"',
            "Пол": "Ж",
            "Возраст": 30,
            "iSayMail": "00000000-1111-2222-3333-444444444444@i.inb.youthink.dev",
            "Reward": 150,
            "Source": "source_one",
        }
    )
