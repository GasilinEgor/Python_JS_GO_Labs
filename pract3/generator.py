import random
import uuid
import ipaddress
from datetime import datetime


def generate_uuid(unique_count: int) -> list[uuid.UUID]:
    return [uuid.uuid4() for _ in range(unique_count)]


def generate_ipv4() -> str:
    ip_number = random.randint(1, 2 ** 32 - 1)
    return str(ipaddress.IPv4Address(ip_number))


def generate_port() -> int:
    return random.randint(1, 65535)


def generate_record(uuid_pool: list[uuid.UUID]) -> dict:
    record = {
        "field_id": random.choice(uuid_pool),
        "ip": generate_ipv4(),
        "port": generate_port(),
        "added_at": datetime.utcnow()
    }
    return record


def generate_batch(batch_size: int, uuid_pool: list[uuid.UUID]) -> list[dict]:
    return [generate_record(uuid_pool) for _ in range(batch_size)]


if __name__ == "__main__":
    uuid_pool = generate_uuid(2)
    res = generate_batch(5, uuid_pool)
    for r in res:
        print(r)
