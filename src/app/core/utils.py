import hashlib
from uuid import UUID, uuid4
from typing import Literal


def generate_id(
        prefix: Literal["USER", "IMAGE", "IMAGELABEL"]
    ) -> str:
    raw_id: UUID = uuid4()
    id: str = f"{prefix}-{str(raw_id)}"
    return id


def hash_ip(ip: str) -> str:
    return hashlib.sha256(ip.encode()).hexdigest()