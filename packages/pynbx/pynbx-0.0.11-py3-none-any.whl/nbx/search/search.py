import os

from pathlib import Path
from typing import List, Tuple

from nbx import config
from nbx.note import Note, Record

SEARCH_OPTIONS = [
    "regex",
    "whoosh",
    "faiss"
]


def search_notes(
    notes: List[Note],
    query: str,
    method: str = "regex"
) -> Tuple[List[Record], List[Note]]:
    # Query are searched in lowercased
    query = query.lower().strip()

    def fallback_func():
        print("[Warning] Falling back to regex search")
        return search_notes(notes, query, "regex")

    # MOCK & Regex are simple
    if os.getenv("DEBUG", "False") == "True":
        from .mock import find_match
        return find_match(notes, query)
    elif method == "regex":
        from .regex import find_match
        return find_match(notes, query)

    # Search with index
    nbx_config = config.load_config()
    notes_dir = nbx_config["notes_dir"]
    if method == "whoosh":
        from .whoosh import find_match
        index_dir = Path(notes_dir, "whoosh")
        return find_match(query, index_dir, notes_dir)
    elif method == "faiss":
        from .faiss import find_match
        index_dir = Path(notes_dir, "faiss")
        return find_match(query, index_dir, notes_dir)
    elif method == "txtai":
        from .txtai import find_match
        find_match(notes, query)
    elif method.startswith("openai"):
        from .openai import find_match
        model = method.split("-", 1)[1]

        def openai_search_func(*args, **kwargs):
            find_match(*args, *kwargs, model=model)

        return openai_search_func(notes, query)
    else:
        return [], []


def index_notes(notes: List[Note], method: str = "regex") -> None:
    print(f"[Info] Indexing using {method}")
    if method == "whoosh":
        from .whoosh import index_notes
        notes_dir = config.load_config()["notes_dir"]
        index_notes(notes, Path(notes_dir, "whoosh"))
    elif method == "faiss":
        from .faiss import index_notes
        notes_dir = config.load_config()["notes_dir"]
        index_notes(notes, Path(notes_dir, "faiss"))
    return
