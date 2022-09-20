import json
import random
import uuid
from time import sleep

from kafka import KafkaProducer

users = [uuid.uuid4() for _ in range(100)]
films = [uuid.uuid4() for _ in range(1000)]


def main():
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    try:
        while True:
            k, v = event_data()
            data = producer.send(
                topic='views',
                value=bytes(v, 'utf-8'),
                key=bytes(k, 'utf-8'),
            )
            print(v)

            sleep(random.randrange(0, 10))
    except KeyboardInterrupt as e:
        print(e)


def event_data() -> tuple:
    user = random.choice(users)
    film = random.choice(films)
    total = random.randrange(1800, 7200, 600)
    progress = random.randrange(0, total)

    val = {
        "user_id": str(user),
        "movie_id": str(film),
        "time": progress,
        "total_time": total
    }
    return (
        f"{user}::{film}", json.dumps(val)
    )


if __name__ == "__main__":
    main()
