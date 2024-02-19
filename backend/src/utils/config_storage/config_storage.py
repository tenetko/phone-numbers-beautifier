import json


class ConfigStorage:
    @classmethod
    def get_config(cls):
        with open("src/utils/config_storage/config.json", "r", encoding="utf-8") as input_file:
            return json.load(input_file)
