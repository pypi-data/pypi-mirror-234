import lancedb
import pyarrow as pa
from pathlib import Path
from datetime import datetime

from nbx import config

MODEL_CKPT = "flax-sentence-embeddings/all_datasets_v3_mpnet-base"
EMBEDDING_SIZE = 768


def get_all_links():
    links_dir = Path(config.load_config()["links_dir"])
    links_dir.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(links_dir)
    table_names = sorted(filter(lambda x: x.startswith("links-"), db.table_names()))
    if len(table_names) == 0:
        return []
    tb = db.open_table(table_names[-1])
    all_links = []
    for row in tb.to_pandas().itertuples(index=False):
        all_links.append((row[0], row[1], row[2], row[3], row[4].strftime("%Y-%m-%d")))
    return all_links


def index_all_links():
    pass


def add_link(link: str, note: str = "") -> None:
    links_dir = Path(config.load_config()["links_dir"])
    links_dir.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(links_dir)
    table_names = sorted(filter(lambda x: x.startswith("links-"), db.table_names()))
    if len(table_names) == 0:
        db.create_table(
            "links-0",
            schema=pa.schema([
                pa.field("link", pa.utf8()),
                pa.field("title", pa.utf8()),
                pa.field("description", pa.utf8()),
                pa.field("note", pa.utf8()),
                pa.field("last_view", pa.timestamp("us")),
                pa.field("embedding", pa.list_(pa.float32(), EMBEDDING_SIZE)),
            ]))
        table_names = ["links-0"]
    idx = len(table_names) - 1
    tb = db.open_table(f"links-{idx}")
    tb.add([{
        "link": link,
        "title": "link_title",
        "description": "link_description",
        "note": note,
        "last_view": datetime.now(),
        "embedding": [0.0 for _ in range(EMBEDDING_SIZE)],
    }])
