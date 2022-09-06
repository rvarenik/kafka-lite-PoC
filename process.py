from contextlib import closing
from time import time_ns

from kafka_lite.consumer import Consumer

NUM_RECORDS = 100_000


def receive():
    with closing(Consumer("test", 0)) as consumer:
        start = time_ns()
        while True:
            id_, data = consumer.receive()
            if id_ == NUM_RECORDS - 1:
                latency = int(time_ns() - data["ts"])
                break
        end = time_ns()
        run_time = int((end - start) // 1e6)
        print(f"it took {run_time} ms, {latency=} ns")


if __name__ == "__main__":
    receive()
