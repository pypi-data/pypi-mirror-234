import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple


from nbx import config, util
from nbx.note import Note, Record, create_note_file

ALL_NOTES = []


def get_all_notes() -> List[Note]:
    nbx_config = config.load_config()
    notes_dir = Path(nbx_config["notes_dir"])
    note_files = notes_dir.glob("*.json")
    note_files = sorted(note_files, reverse=True)
    notes = []
    for note_file in note_files:
        notes.append(Note(note_file))
    return notes


def get_alias_headlines() -> Dict:  # {"alias_name": "note_headline"}
    alias_headlines = {}
    all_notes = get_all_notes()
    for note in all_notes:
        if note.alias:
            headline = note.get_headline()
            alias_headlines[note.alias] = headline
    return alias_headlines


def get_note_by_alias(alias: str) -> Note:
    alias = alias.strip()
    notes = get_all_notes()
    for note in notes:
        if note.alias == alias:
            return note
    return None


def get_note(index: str) -> Note:
    index = index.strip()
    note = None
    if index.isnumeric():
        index = int(index)
        notes = get_all_notes()
        if len(notes) > index:
            note = notes[index]
    else:
        note = get_note_by_alias(index)
    return note


def create_alias(note: Note, alias: str):
    note.update_alias(alias)
    note.save()


def delete_alias(alias: str):
    all_notes = get_all_notes()
    for note in all_notes:
        if note.alias == alias:
            note.update_alias("")
            note.save()
            break


def create_note(content: str) -> Path:
    nbx_config = config.load_config()
    notes_dir = Path(nbx_config["notes_dir"])
    note_file_path = create_note_file(content, notes_dir)
    return note_file_path


def search_notes(notes: List[Note], query: str) -> Tuple[List[Record], List[Note]]:
    from nbx import search
    nbx_config = config.load_config()
    search_method = nbx_config["search_method"]
    return search.search_notes(notes, query, search_method)


def find_relevant_records(content: str) -> List[List[str]]:
    """
    Find abstracts of relevant note based on content around the cursor.

    Output: [{"heading": "Note Title", "headingId": "123456", "content": "Note Paragraph"},...]
    """
    global ALL_NOTES
    if not ALL_NOTES:
        ALL_NOTES = get_all_notes()
    if len(content) < 10:
        return []
    try:
        records, notes = search_notes(ALL_NOTES, content)
    except Exception:
        records = []
    result = []
    for record in records:
        result.append(vars(record))
    return result


def add_image(image: Any) -> str:
    nbx_config = config.load_config()
    notes_dir = Path(nbx_config["notes_dir"])
    images_dir = Path(notes_dir, "images")
    images_dir.mkdir(parents=True, exist_ok=True)
    image_name = f"{str(uuid.uuid4())}.png"
    image_path = Path(notes_dir, "images", image_name)
    util.save_base64(image, image_path)
    return image_name


def get_image_path(filename: str) -> Path:
    nbx_config = config.load_config()
    notes_dir = Path(nbx_config["notes_dir"])
    image_path = Path(notes_dir, "images", filename)
    return image_path


def index_notes(notes: List[Note]) -> None:
    from nbx import search
    nbx_config = config.load_config()
    search_method = nbx_config["search_method"]
    search.index_notes(notes, search_method)


def index_all_notes(background: bool = False) -> Note:
    if background:
        import subprocess
        subprocess.Popen(["nbx", "index"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    else:
        all_notes = get_all_notes()
        index_notes(all_notes)
