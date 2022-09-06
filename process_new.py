import sys
from contextlib import closing

from kafka_lite.consumer import Consumer


def receive(consumer_id: int):
    with closing(Consumer("test", consumer_id)) as consumer:
        while True:
            id_, data = consumer.receive()
            print(f"new record id={id_}: {data['msg']}")
            consumer.ack(id_)


if __name__ == "__main__":
    consumer_id = int(sys.argv[1]) if len(sys.argv) == 2 else 42
    receive(consumer_id)
