import lancedb
import pyarrow as pa
from typing import List, Tuple
from datetime import datetime
from pathlib import Path

from nbx import config

MODEL_CKPT = "flax-sentence-embeddings/all_datasets_v3_mpnet-base"
EMBEDDING_SIZE = 768


def get_gists_table_name() -> str:
    gists_dir = Path(config.load_config()["gists_dir"])
    gists_dir.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(gists_dir)
    table_names = sorted(filter(lambda x: x.startswith("gists-"), db.table_names()))
    if len(table_names) == 0:
        return ""
    return table_names[-1]


def add_gist(gist: str, comment: str = "") -> None:
    gists_dir = Path(config.load_config()["gists_dir"])
    gists_dir.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(gists_dir)
    table_names = sorted(filter(lambda x: x.startswith("gists-"), db.table_names()))
    if len(table_names) == 0:
        db.create_table(
            "gists-0",
            schema=pa.schema([
                pa.field("gist", pa.utf8()),
                pa.field("comment", pa.utf8()),
                pa.field("updated_at", pa.timestamp("us")),
                pa.field("embedding", pa.list_(pa.float32(), EMBEDDING_SIZE)),
            ]))
        table_names = ["gists-0"]
    idx = len(table_names) - 1
    tb = db.open_table(f"gists-{idx}")
    tb.add([{
        "gist": gist,
        "comment": comment,
        "updated_at": datetime.now(),
        "embedding": [0.0 for _ in range(EMBEDDING_SIZE)],
    }])


def get_all_gists() -> List[Tuple[str, str]]:
    gists_dir = Path(config.load_config()["gists_dir"])
    gists_dir.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(gists_dir)
    table_names = sorted(filter(lambda x: x.startswith("gists-"), db.table_names()))
    if len(table_names) == 0:
        return []
    tb = db.open_table(table_names[-1])
    all_gists = []
    for row in tb.to_pandas().itertuples(index=False):
        all_gists.append((row[0], row[1], row[2].strftime("%Y-%m-%d")))
    return all_gists


def index_all_gists() -> None:
    from sentence_transformers import SentenceTransformer
    gists_dir = Path(config.load_config()["gists_dir"])
    gists_dir.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(gists_dir)
    table_names = sorted(filter(lambda x: x.startswith("gists-"), db.table_names()))
    if len(table_names) == 0:
        return
    prev_table_name = table_names[-1]
    curr_table_name = f"gists-{len(table_names)}"
    gists = db.open_table(prev_table_name).to_arrow().to_pylist()
    model = SentenceTransformer(MODEL_CKPT)
    # step 1: create new table with embedding
    data = []
    for gist in gists:
        embedding = model.encode([gist["gist"] + " " + gist["comment"]])[0]
        data.append({
            "gist": gist["gist"],
            "comment": gist["comment"],
            "updated_at": gist["updated_at"],
            "embedding": embedding
        })
    db.create_table(curr_table_name, data, schema=pa.schema([
        pa.field("gist", pa.utf8()),
        pa.field("comment", pa.utf8()),
        pa.field("updated_at", pa.timestamp("us")),
        pa.field("embedding", pa.list_(pa.float32(), EMBEDDING_SIZE)),
    ]))
    # step 2: index the text based columns
    tb = db.open_table(curr_table_name)
    tb.create_fts_index(["gist", "comment"])
    return


def search_gist_embedding(query: str):
    from sentence_transformers import SentenceTransformer
    gists_dir = Path(config.load_config()["gists_dir"])
    gists_dir.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(gists_dir)
    table_names = sorted(filter(lambda x: x.startswith("gists-"), db.table_names()))
    if len(table_names) == 0:
        return []
    gists = db.open_table(table_names[-1])
    model = SentenceTransformer(MODEL_CKPT)
    query_embedding = model.encode(query)
    result = gists.search(query_embedding, vector_column_name="embedding").to_arrow().to_pylist()
    return result


def search_gist_text(query: str):
    gists_dir = Path(config.load_config()["gists_dir"])
    gists_dir.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(gists_dir)
    table_names = sorted(filter(lambda x: x.startswith("gists-"), db.table_names()))
    if len(table_names) == 0:
        return []
    gists = db.open_table(table_names[-1])
    result = gists.search(query).to_arrow().to_pylist()
    return result


def del_gist(idx: int):
    gists_table_name = get_gists_table_name()
    if not gists_table_name:
        return
    gists_dir = Path(config.load_config()["gists_dir"])
    gists = get_all_gists()
    if idx < 0 or idx >= len(gists):
        return
    db = lancedb.connect(gists_dir)
    tb = db.open_table(gists_table_name)
    tb.delete(f"gist='{gists[idx][0]}' and comment='{gists[idx][1]}'")


def edit_gist(idx: int):
    return


def peek_gist(query: str):
    return
