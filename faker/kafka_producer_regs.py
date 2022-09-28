import json
import random
import uuid
from time import sleep

from faker import Faker
from kafka import KafkaProducer


def main():
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    try:
        while True:
            k, v = event_data()
            data = producer.send(
                topic='registred',
                value=bytes(v, 'utf-8'),
                key=bytes(k, 'utf-8'),
            )
            print(v)

            sleep(random.randrange(120, 300))
    except KeyboardInterrupt as e:
        print(e)


def event_data() -> tuple:
    fake = Faker()
    user = uuid.uuid4()
    login = fake.user_name()
    val = {
        "user_id": str(user),
        "login": login,
        "email": f"{login}@{fake.free_email_domain()}",
    }
    return (
        f"{user}", json.dumps(val)
    )


if __name__ == "__main__":
    main()
