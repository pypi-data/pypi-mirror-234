import uuid
from typing import List, Tuple

from faker import Faker

from nbx.note import Note, Record


def find_match(*args, **kwargs) -> Tuple[List[Record], List[Note]]:
    Faker.seed(0)
    fake = Faker()

    records = []
    notes = []
    for _ in range(kwargs.get("num", 20)):
        records.append(Record(str(uuid.uuid4()), fake.text()[:8], fake.text()))
        notes.append(fake.file_path())

    return records, notes
