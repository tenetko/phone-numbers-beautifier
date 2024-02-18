from datetime import datetime

import pandas as pd
import pytz

from src.core.tzb_template_parser.tzb_template_parser import TZBTemplateParser
from src.tests.tzb_template_parser.fixtures import *

template_parser = TZBTemplateParser()


def test_convert_date_time_to_moscow_timezone():
    raw_date = "Mon, 01 Jan 2024 13:58:30 GMT"
    result = template_parser.convert_date_time_to_moscow_timezone(raw_date)
    expected_result = datetime(2024, 1, 1, 13, 58, 30, 0, pytz.UTC).astimezone((pytz.timezone("Europe/Moscow")))

    assert result == expected_result


def test_get_date_from_date_time():
    raw_date = "Mon, 01 Jan 2024 13:00:00 GMT"
    date_time = template_parser.convert_date_time_to_moscow_timezone(raw_date)
    result = template_parser.get_date_from_date_time(date_time)
    expected_result = "2024-01-01"

    assert result == expected_result


def test_get_date_from_date_time_late_night_case():
    # Moscow is 3 hours ahead of GMT/UTC
    raw_date = "Mon, 31 Dec 2023 22:00:00 GMT"
    date_time = template_parser.convert_date_time_to_moscow_timezone(raw_date)
    result = template_parser.get_date_from_date_time(date_time)
    expected_result = "2024-01-01"

    assert result == expected_result


def test_make_filtered_source_dataframe(source_dataframe, expected_source_dataframe):
    raw_date_from = "Mon, 11 Jan 2024 01:02:03 GMT"
    raw_date_to = "Mon, 12 Jan 2024 04:05:06 GMT"
    date_from = template_parser.get_date(raw_date_from)
    date_to = template_parser.get_date(raw_date_to)
    result = template_parser.make_filtered_source_dataframe(source_dataframe, date_from, date_to)
    expected_result = expected_source_dataframe

    assert result.equals(expected_result)
