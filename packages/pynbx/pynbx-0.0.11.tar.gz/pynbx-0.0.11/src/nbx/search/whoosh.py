import os
from datetime import datetime
from typing import List, Tuple
from pathlib import Path

from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

from nbx.note import Note, Record


def find_match(
    query: str,
    index_dir: Path,
    notes_dir: Path,
    top_k: int = 10
) -> Tuple[List[Record], List[Note]]:
    if not index_dir.exists():
        print("No index found, please index the notebase first: nbx index")
        return [], []

    # get the index with the latest timestamp
    indices = [f.path for f in os.scandir(index_dir) if f.is_dir() and f.name.startswith("index_")]
    indices = sorted(indices, reverse=True)
    if len(indices) == 0:
        print("No index found, please index the notebase first: nbx index")
        return [], []

    ix = open_dir(indices[0])
    with ix.searcher() as searcher:
        parser = QueryParser("content", ix.schema)
        myquery = parser.parse(query)
        results = searcher.search(myquery, limit=top_k)
        # convert results to records & notes
        res_records = []
        res_notes = []
        loaded_notes = {}
        loaded_records = {}
        for result in results:
            id = result["id"]
            timestamp = id.split("#")[0]
            record_idx = int(id.split("#")[1])
            note_file_path = Path(notes_dir, f"{timestamp}.json")
            if note_file_path not in loaded_notes:
                note = Note(note_file_path)
                loaded_notes[note_file_path] = note
                loaded_records[note_file_path] = note.get_sections()
            note = loaded_notes[note_file_path]
            record = loaded_records[note_file_path][record_idx]
            res_records.append(record)
            res_notes.append(note)

    return res_records, res_notes


# https://whoosh.readthedocs.io/en/latest/quickstart.html
def index_notes(notes: List[Note], index_dir: Path) -> None:
    index_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    current_index_dir = Path(index_dir, f"index_{timestamp}")
    current_index_dir.mkdir(parents=True, exist_ok=True)

    # create the index
    schema = Schema(id=ID(stored=True), heading=TEXT, content=TEXT)
    ix = create_in(current_index_dir, schema)

    # add documents
    writer = ix.writer()
    for note in notes:
        for record in note.get_sections():
            writer.add_document(
                id=record.id,
                heading=record.heading.lower(),
                content=record.content.lower()
            )
    writer.commit()
