import shutil
import tempfile
import time
from pathlib import Path

from nbx.note import Note, create_note_file

NOTES_HTML = [
    "./notes/title_heading_content.html",
    "./notes/only_heading.html",
    "./notes/heading_heading.html"
]

KEYWORD_QUERY = "title_heading_content"
NON_EXIST_QUERY = "shouldn't exist"


def test_search_regex():
    from nbx.search.regex import find_match

    notes_dir = Path(tempfile.mkdtemp())

    # create notes_file
    notes = []
    for note_html in NOTES_HTML:
        with open(note_html) as file:
            note_path = create_note_file(file.read(), notes_dir)
        note = Note(note_path)
        notes.append(note)
        time.sleep(1.5)  # sleep 1.5 second, otherwise notes will have the same timestamp

    # test find_match
    res_sections, res_notes = find_match(notes, KEYWORD_QUERY)
    assert len(res_sections) > 0
    # QUERY is an excerpt from the first record of the title_heading_content
    first_note = res_notes[0]
    assert res_sections[0].id == f"{first_note.last_update}#0"

    # this query shouldn't return any matched result
    res_sections, res_notes = find_match(notes, NON_EXIST_QUERY)
    assert len(res_sections) == 0

    # cleanup the temporary notes directory
    shutil.rmtree(notes_dir)


if __name__ == "__main__":
    test_search_regex()
