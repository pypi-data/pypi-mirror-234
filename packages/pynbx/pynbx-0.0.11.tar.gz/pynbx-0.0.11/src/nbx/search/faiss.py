import os
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

from nbx import util
from nbx.note import Note, Record

MODEL_CKPT = "flax-sentence-embeddings/all_datasets_v3_mpnet-base"


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
    index_files = index_dir.glob("*.index")
    index_files = sorted(index_files, reverse=True)
    if len(index_files) == 0:
        print("No index found, please index the notebase first: nbx index")
        return [], []

    # check index_file and the corresponding info json
    index_file = index_files[0]
    index_timestamp = index_file.name.split(".")[0]
    index_info_file = Path(index_dir, f"{index_timestamp}.json")
    if not index_info_file.exists():
        print("Corrupted index, please re-index the notebase first: nbx index")
        return [], []

    # load faiss index
    index_path = os.fspath(index_file)
    index = faiss.read_index(index_path)

    # create the search vector for the query
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    encoder = SentenceTransformer(MODEL_CKPT)
    vector = encoder.encode(query)
    _vector = np.array([vector])
    faiss.normalize_L2(_vector)
    top_k = min(top_k, index.ntotal)
    distances, ann = index.search(_vector, k=top_k)

    # get record(section) ids
    index_info = util.load_json(index_info_file)
    res_records = []
    res_notes = []
    loaded_notes = {}
    loaded_records = {}
    for ann_idx in ann[0]:
        record_id = index_info[str(ann_idx)]
        note_id = record_id.split("#")[0]
        record_idx = int(record_id.split("#")[1])
        if note_id not in loaded_notes:
            note = Note(Path(notes_dir, f"{note_id}.json"))
            loaded_notes[note_id] = note
            loaded_records[note_id] = note.get_sections()
        note = loaded_notes[note_id]
        record = loaded_records[note_id][record_idx]
        res_records.append(record)
        res_notes.append(note)

    return res_records, res_notes


def index_notes(notes: List[Note], index_dir: Path = "") -> None:
    # create index_dir if doesn't exist
    index_dir.mkdir(parents=True, exist_ok=True)

    # convert notes content into a dataframe
    data = []
    for note in notes:
        for record in note.get_sections():
            data.append([record.content, record.id])
    df = pd.DataFrame(data, columns=["text", "id"])

    # no need to index if no note exists yet
    if len(data) == 0:
        return

    # create vector from the text
    encoder = SentenceTransformer(MODEL_CKPT)
    vectors = encoder.encode(df["text"])

    # build the faiss index from the vectors
    vector_dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(vector_dimension)
    faiss.normalize_L2(vectors)
    index.add(vectors)

    # save the index to disk
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    index_path = os.fspath(Path(index_dir, f"{timestamp}.index"))
    faiss.write_index(index, index_path)
    # save some additional info
    info_path = os.fspath(Path(index_dir, f"{timestamp}.json"))
    util.save_json_obj(info_path, df["id"].to_dict())
