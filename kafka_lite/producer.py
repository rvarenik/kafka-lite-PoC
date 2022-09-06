import os
from contextlib import suppress
from json import dumps, loads
from time import time_ns


class Producer:
    def __init__(self, topic: str):
        file_name = f"{topic}.000"
        self.id = self._find_last_record_id(file_name)
        print(f"Last record id = {self.id}")
        self.topic_file = open(file_name, "at", buffering=1, encoding="ascii")

    @staticmethod
    def _find_last_record_id(file_name: str) -> int:
        last_id = 0
        with suppress(FileNotFoundError):
            with open(file_name, "rt", buffering=1) as topic_file:
                last_line = None
                while True:
                    if raw_line := topic_file.readline():
                        last_line = raw_line
                    else:
                        break
            if last_line:
                data = loads(last_line)
                last_id = data["id"] + 1
        return last_id

    def close(self):
        self.topic_file.close()

    def send(self, msg: dict) -> None:
        data = {
            "id": self.id,
            "ts": time_ns(),
            "payload": msg,
        }
        self.topic_file.write(dumps(data, ensure_ascii=True) + os.linesep)
        self.id += 1
