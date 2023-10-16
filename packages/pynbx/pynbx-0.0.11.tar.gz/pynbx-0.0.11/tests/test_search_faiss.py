import shutil
import tempfile
import time
from pathlib import Path

from nbx.note import Note, create_note_file

NOTE_WITH_TITLE = """<h1>Test note with title</h1><p>This is a description right after the note title and before the first h2 heading. This section performs as an abstraction or introduction area of the entire note.</p><h2>First section</h2><p>This is the first section that user can jot down more detailed information that is contained as a section. Each section should be self-containable in terms of the logic. Then the user can restitch the section with other sections into a full complete note without much modification to the content.</p><h2>Second section</h2><p>Here is the second section of the note. As mentioned earlier, each section should be self-containable in terms of logic. This second section should talk about some thing different from the first section.</p><p>Each section may contain more than one paragraph. As long as the entire section is complete in terms of the logic. </p><h2>Section with bullet points</h2><p>A second could also contain contents other than test, for example bullet points</p><ol><li><p>The first item in the list</p></li><li><p>The second item in the list</p></li></ol>"""  # noqa: E501
NOTE_WITHOUT_TITLE = """<p>Note without title. Sometime there are unformalized notes that don't really have a title. We should be able to put this kind of notes also part of the searchable content.</p><h2>First section</h2><p>Even though the note doesn't have a title, it might still have sections.</p>"""  # noqa: E501
QUERY = "We should be able to put this kind of notes also part of the searchable content"


def test_search_faiss():
    from nbx.search.faiss import index_notes, find_match

    # test index_notes
    notes_dir = Path(tempfile.mkdtemp())
    note_with_title_path = create_note_file(NOTE_WITH_TITLE, notes_dir)
    note_with_title = Note(note_with_title_path)
    time.sleep(1.5)  # sleep 1.5 second, otherwise the generated notes will have the same timestamp
    note_without_title_path = create_note_file(NOTE_WITHOUT_TITLE, notes_dir)
    note_without_title = Note(note_without_title_path)
    notes = [note_with_title, note_without_title]
    index_dir = Path(notes_dir, "faiss")
    index_notes(notes, index_dir)

    records_cnt = 0
    for note in notes:
        records_cnt += len(note.get_sections())

    # test find_match
    res_records, res_notes = find_match(QUERY, index_dir, notes_dir, top_k=records_cnt)

    assert len(res_records) == records_cnt
    assert len(res_notes) == len(res_records)
    # QUERY is an excerpt from the first record of the note_without_title
    assert res_records[0].id == f"{note_without_title.last_update}#0"
    # cleanup the temporary notes directory
    shutil.rmtree(notes_dir)


if __name__ == "__main__":
    test_search_faiss()
