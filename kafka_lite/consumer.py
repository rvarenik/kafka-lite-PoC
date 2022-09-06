import os
from contextlib import suppress
from json import loads, dumps
from time import time_ns
from typing import Optional


class Consumer:
    def __init__(self, topic: str, consumer_id: int):
        file_name = f"./{topic}.000"
        ack_file_name = f"./{topic}.000.ack"
        self.consumer_id = consumer_id
        self.ack_topic = open(ack_file_name, "at", buffering=1)
        # create topic file if hasn't been created yet
        with open(file_name, "at"):
            ...
        self.data_topic = open(file_name, "rt", buffering=1)
        last_ack = self._find_last_ack(ack_file_name, consumer_id)
        self._skip_acked(last_ack)

    def close(self):
        self.data_topic.close()
        self.ack_topic.close()

    def skip_to(self, msg_id: int) -> None:
        raise NotImplemented

    def has_messages(self) -> bool:
        raise NotImplemented

    def receive(self):
        raw_line = None
        while not raw_line:
            raw_line = self.data_topic.readline()
        data = loads(raw_line)
        return data["id"], data["payload"]

    def ack(self, msg_id: int) -> None:
        ack_data = {
            "id": msg_id,
            "consumer": self.consumer_id,
            "ts": time_ns(),
        }
        self.ack_topic.write(dumps(ack_data) + os.linesep)

    def _find_last_ack(self, ack_file_name: str, consumer_id: int) -> Optional[int]:
        last_ack = None
        with suppress(FileNotFoundError):
            with open(ack_file_name, "rt", buffering=1) as ack_topic:
                raw_line = ack_topic.readline()
                while raw_line:
                    data = loads(raw_line)
                    if data["consumer"] == consumer_id:
                        last_ack = data["id"]
                    raw_line = ack_topic.readline()
        return last_ack

    def _skip_acked(self, last_ack: int) -> None:
        current_id = None
        while current_id != last_ack:
            raw_line = self.data_topic.readline()
            assert raw_line is not None
            current_id = loads(raw_line)["id"]
