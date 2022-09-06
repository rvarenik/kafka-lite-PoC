from contextlib import closing
from time import time_ns

from kafka_lite.producer import Producer

NUM_RECORDS = 100_000


def send():
    with closing(Producer("test")) as producer:
        start = time_ns()
        for i in range(NUM_RECORDS):
            data = {
                "msg": "test",
                "ts": time_ns(),
            }
            producer.send(data)
        end = time_ns()
        run_time = int((end - start) // 1e6)
        print(f"it took {run_time} ms")


if __name__ == "__main__":
    send()
