import re
from typing import List, Tuple

from nbx.note import Note, Record


def appear_in_record(query: str, record: Record) -> bool:
    content = record.content
    heading = record.heading
    return re.search(query, content) or re.search(query, heading)


def find_match(notes: List[Note], query: str) -> Tuple[List[Record], List[Note]]:
    res_records = []
    res_notes = []
    for note in notes:
        for record in note.get_sections():
            if appear_in_record(query, record):
                res_records.append(record)
                res_notes.append(note)
    return res_records, res_notes
