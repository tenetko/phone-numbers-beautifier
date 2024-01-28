from src.core.tzb_template_parser.tzb_template_parser import TZBTemplateParser

template_parser = TZBTemplateParser()

def test_source_getter(quotas_dataframe):
    result = quotas_parser.make_quotas_dictionary(quotas_dataframe)
    expected_result = defaultdict(dict, QUOTAS_PARSER_MOCK_DATA["quotas_config"])

    assert result == expected_result
