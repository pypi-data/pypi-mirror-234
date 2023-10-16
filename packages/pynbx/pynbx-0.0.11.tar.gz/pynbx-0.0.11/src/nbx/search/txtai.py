from typing import List, Tuple

from txtai.embeddings import Embeddings

from nbx.note import Note, Record


MODEL_CKPT = "sentence-transformers/nli-mpnet-base-v2"


# https://github.com/neuml/txtai/blob/master/examples/similarity.py
def find_match(notes: List[Note], query: str) -> Tuple[List[Record], List[Note]]:
    embedding = Embeddings({"path": MODEL_CKPT})
    res_records = []
    res_notes = []
    data = []
    record_note = []
    for note in notes:
        for record in note.get_sections():
            text_data = record.heading + record.content
            data.append(text_data)
            record_note.append([record, note])
    results = embedding.similarity(query, data)
    results = results[:10] if len(results) > 10 else results
    for result in results:
        res_id = result[0]
        res_records.append(record_note[res_id][0])
        res_notes.append(record_note[res_id][1])
    return res_records, res_notes
