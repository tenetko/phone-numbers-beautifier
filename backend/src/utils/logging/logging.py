import json


class Sink:
    def __init__(self):
        self.records = []

    def write(self, message):
        data = json.loads(message)
        record = f"{data['record']['message']}"
        self.records.append(record)
