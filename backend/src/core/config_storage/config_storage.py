import json


class ConfigStorage:
    def __init__(self):
        self.config = self.get_config()

    def get_config(self):
        with open("src/core/config_storage/config.json", "r", encoding="utf-8") as input_file:
            return json.load(input_file)

    def provide_config(self):
        return self.config
