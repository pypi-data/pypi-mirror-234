import glob
import shutil
import tempfile
import os
import time
from pathlib import Path

from bs4 import BeautifulSoup

from nbx.note import Note, create_note_file

NOTE_HTML_FILES = [
    "./notes/content_heading.html",
    "./notes/heading_content_heading.html",
    "./notes/heading_content.html",
    "./notes/heading_heading.html",
    "./notes/only_content_lists.html",
    "./notes/only_content.html",
    "./notes/only_heading.html",
    "./notes/only_title.html",
    "./notes/title_content_heading_heading.html",
    "./notes/title_content_heading.html",
    "./notes/title_content_lists.html",
    "./notes/title_content.html",
    "./notes/title_heading_content_heading_heading.html",
    "./notes/title_heading_content.html"
]

NOTE_TITLES = [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "Title: only_title",
    "Title: title_content_heading_heading",
    "Title: title_content_heading",
    "Title: title_content_lists",
    "Title: title_content",
    "Title: title_heading_content_heading_heading",
    "Title: title_heading_content"
]

NOTE_SECTION_CNTS = [2, 2, 1, 2, 1, 1, 1, 1, 3, 2, 1, 1, 4, 2]

NOTE_HEADLINES = [
    "This is the paragraph of the content",
    "A section heading",
    "A section heading",
    "A section heading",
    "list content item 1\nlist content item 2\nlist content item 3",
    "The note could only contain a short paragraph as the content. Normally this\n  kind of notes is added via nbx add -m",  # noqa: E501
    "Only a section heading",
    "Title: only_title",
    "Title: title_content_heading_heading",
    "Title: title_content_heading",
    "Title: title_content_lists",
    "Title: title_content",
    "Title: title_heading_content_heading_heading",
    "Title: title_heading_content"
]


def _note_update_body(note_file: Path):
    # setup
    notes_dir = Path(tempfile.mkdtemp())
    with open(note_file) as file:
        note_path = create_note_file(file.read(), notes_dir)
    note = Note(note_path)
    original_title = note.get_title()
    original_body = BeautifulSoup(note.get_body(), features="html.parser").prettify()
    updated_body = BeautifulSoup(
        "<p>updated paragraph body by test_note_update_body</p>",
        features="html.parser"
    ).prettify()
    note.update_body(updated_body)
    # check whether the temporary html file exists
    tmp_html_file = Path(notes_dir, ".tmp", f"{note.last_update}.html")
    assert tmp_html_file.exists(), "Temporary html file doesn't exist after update"
    # check whether the original disk note file unmodified
    original_note = Note(note_path, cache=False)
    modified_err_msg = f"Original disk file got modifed while updating {note_file}"
    assert original_note.get_title() == original_title, modified_err_msg
    original_note_body = BeautifulSoup(original_note.get_body(), features="html.parser").prettify()
    assert original_note_body == original_body, modified_err_msg
    # check whether newly loaded note has the updated body
    new_note = Note(note_path)
    load_err_msg = f"Newly loaded note doesn't have the update while updating {note_file}"
    assert new_note.get_title() == original_title, load_err_msg
    assert new_note.get_body() == updated_body, load_err_msg
    # check whether the tempoary html file has the right title
    with open(tmp_html_file) as html_file:
        tmp_html = BeautifulSoup(html_file.read(), features="html.parser")
    if tmp_html.find("h1"):
        assert tmp_html.find("h1").text.strip() == original_title
        tmp_html.find("h1").decompose()
    assert tmp_html.prettify() == updated_body


def test_note_update_body():
    for note_file in NOTE_HTML_FILES:
        _note_update_body(note_file)


def _note_update_title_titled(note_file: Path):
    # setup
    notes_dir = Path(tempfile.mkdtemp())
    with open(note_file) as file:
        note_path = create_note_file(file.read(), notes_dir)
    note = Note(note_path)
    original_title = note.get_title()
    original_body = BeautifulSoup(note.get_body(), features="html.parser").prettify()
    updated_title = "updated title by test_note_update_title"
    note.update_title(updated_title)
    # check whether the temporary html file exists
    tmp_html_file = Path(notes_dir, ".tmp", f"{note.last_update}.html")
    assert tmp_html_file.exists(), "Temporary html file doesn't exist after update"
    # check whether the original disk note file unmodified
    original_note = Note(note_path, cache=False)
    modified_err_msg = f"Original disk file got modifed while updating {note_file}"
    assert original_note.get_title() == original_title, modified_err_msg
    original_note_body = BeautifulSoup(original_note.get_body(), features="html.parser").prettify()
    assert original_note_body == original_body, modified_err_msg
    # check whether newly loaded note has the updated title
    new_note = Note(note_path)
    load_err_msg = f"Newly loaded note doesn't have the update while updating {note_file}"
    assert new_note.get_title() == updated_title, load_err_msg
    assert new_note.get_body() == original_body, load_err_msg
    # check whether the tempoary html file has the right title
    with open(tmp_html_file) as html_file:
        tmp_html = BeautifulSoup(html_file.read(), features="html.parser")
    no_tag_err_msg = f"No h1 tag after title update on {note_file}"
    assert tmp_html.find("h1"), no_tag_err_msg
    mismatch_err_msg = f"H1 tag's string incorrect after title update on {note_file}"
    assert tmp_html.find("h1").text.strip() == updated_title, mismatch_err_msg
    # check whether the temporary html has the right body
    tmp_html.find("h1").decompose()
    assert tmp_html.prettify() == original_body
    # cleanup
    shutil.rmtree(notes_dir)


def _note_update_title_untitled(note_file: Path):
    # setup
    notes_dir = Path(tempfile.mkdtemp())
    with open(note_file) as file:
        note_path = create_note_file(file.read(), notes_dir)
    note = Note(note_path)
    original_title = note.get_title()
    original_body = BeautifulSoup(note.get_body(), features="html.parser").prettify()
    note.update_title("")
    # check whether the temporary html file exists
    tmp_html_file = Path(notes_dir, ".tmp", f"{note.last_update}.html")
    assert tmp_html_file.exists(), "Temporary html file doesn't exist after update"
    # check whether the original disk note file unmodified
    original_note = Note(note_path, cache=False)
    modified_err_msg = f"Original disk file got modifed while updating {note_file}"
    assert original_note.get_title() == original_title, modified_err_msg
    original_note_body = BeautifulSoup(original_note.get_body(), features="html.parser").prettify()
    assert original_note_body == original_body, modified_err_msg
    # check whether newly loaded note has the updated title
    new_note = Note(note_path)
    assert new_note.get_title() == "", modified_err_msg
    assert new_note.get_body() == original_body, modified_err_msg
    # check whether the tempoary html file has the right title (no h1 tag)
    with open(tmp_html_file) as html_file:
        tmp_html = BeautifulSoup(html_file.read(), features="html.parser")
    tag_err_msg = f"H1 tag still exist after clearing title in {note_file}"
    assert not tmp_html.find("h1"), tag_err_msg
    # check whether the temporary html has the right body
    assert tmp_html.prettify() == BeautifulSoup(original_body, features="html.parser").prettify()
    # cleanup
    shutil.rmtree(notes_dir)


def test_note_update_title():
    """
    There are several tricky cases for updating a note's title:
    1. From untitled to titled
    2. From titled to titled
    3. From titled to untitled
    """
    # Update with a title
    for note_file in NOTE_HTML_FILES:
        _note_update_title_titled(note_file)
    # Remove the title from the note if exist
    for note_file in NOTE_HTML_FILES:
        _note_update_title_untitled(note_file)


def test_note_save():
    """
    While a note is being updated, a temporary html file with the latest content is generated.
    During the editing, the original note file keeps unmodified.
    After the note is saved by the user, the temporary and original file should be delted.
    A new note file with the update stamp and updated content should appear in the notes folder.
    """
    # setup
    note_file = "./notes/title_heading_content.html"
    notes_dir = Path(tempfile.mkdtemp())
    with open(note_file) as file:
        note_path = create_note_file(file.read(), notes_dir)
    note = Note(note_path)
    # update the note with a different title
    updated_title = "updated title by test_note_save"
    note.update_title(updated_title)
    # check whether the temporary html file exists
    tmp_html_file = Path(notes_dir, ".tmp", f"{note.last_update}.html")
    assert tmp_html_file.exists(), "Temporary html file doesn't exist after update"
    time.sleep(1.5)  # sleep 1.5 second, otherwise the saved note will have the same timestamp
    note.save()
    # check whether the temporary html file is deleted
    assert not tmp_html_file.exists(), "Temporary html file still exist after save"
    # check wehther the old note file is deleted
    assert not note_path.exists(), "Old note still exist after save"
    # check whether the new note file is generated
    files = glob.glob(f"{os.fspath(notes_dir)}/*.json")
    assert len(files) == 1, "New note json file isn't created"
    # check whether the new note file has the right
    updated_note = Note(files[0])
    assert updated_note.get_title() == updated_title, "Saved note doesn't have the right title"
    # cleanup
    shutil.rmtree(notes_dir)


def test_note_mulitple_save():
    """
    If a note got saved multiple times, it should appear as multiple notes.
    Instead, it should only appear 1 note on disk.
    """
    # setup
    note_file = "./notes/title_heading_content.html"
    notes_dir = Path(tempfile.mkdtemp())
    with open(note_file) as file:
        note_path = create_note_file(file.read(), notes_dir)
    note = Note(note_path)
    # update the note with a different title
    updated_title = "updated title by test_note_save"
    note.update_title(updated_title)
    note.save()
    note.save()
    # check whether the new note file is generated
    files = glob.glob(f"{os.fspath(notes_dir)}/*.json")
    assert len(files) == 1
    time.sleep(1.5)  # sleep 1.5 second, otherwise the saved note will have the same timestamp
    note.save()
    note.save()
    # check whether the new note file is generated
    files = glob.glob(f"{os.fspath(notes_dir)}/*.json")
    assert len(files) == 1
    # check whether the new note file has the right
    updated_note = Note(files[0])
    assert updated_note.get_title() == updated_title, "Saved note doesn't have the right title"
    # cleanup
    shutil.rmtree(notes_dir)


def test_note_reset():
    """
    When a note got updated, a temporary html file with the latest content is generated.
    If the quit NBX without saving the file, the temporary file remains there.
    When the note is reset explicitly, the temporary file should be delted.
    """
    # setup
    note_file = "./notes/title_heading_content.html"
    notes_dir = Path(tempfile.mkdtemp())
    with open(note_file) as file:
        note_path = create_note_file(file.read(), notes_dir)
    note = Note(note_path)
    # update the note with a different title
    updated_title = "updated title by test_note_save"
    note.update_title(updated_title)
    # check whether the temporary html file exists
    tmp_html_file = Path(notes_dir, ".tmp", f"{note.last_update}.html")
    assert tmp_html_file.exists(), "Temporary html file doesn't exist after update"
    note.reset()
    # check whether the temporary html file is deleted
    assert not tmp_html_file.exists(), "Temporary html file still exist after save"
    # check whether the note has the original content
    new_note = Note(note_path)
    err_msg = "Note doesn't have the same title after reset"
    assert new_note.get_title() == "Title: title_heading_content", err_msg
    # cleanup
    shutil.rmtree(notes_dir)


def test_note_archive():
    """
    When a note is archived, the note's json file shouldn't appear in the notes directory anymore.
    Instead, it should be moved to the archive folder.
    """
    # setup
    note_file = "./notes/title_heading_content.html"
    notes_dir = Path(tempfile.mkdtemp())
    with open(note_file) as file:
        note_path = create_note_file(file.read(), notes_dir)
    note = Note(note_path)
    note.archive()
    # check whether the note json file is deleted
    assert not note_path.exists(), "Note json file still exist after archive"
    # check wehther the note json file is moved to the archive folder
    archive_note_path = Path(notes_dir, "archive", f"{note.last_update}.json")
    assert archive_note_path.exists(), "Archived json file doesn't exist after archive"
    # check whether the archived note still could be loaded correctly
    archived_note = Note(archive_note_path)
    err_msg = "Archived note could not be loaded correctly"
    assert archived_note.get_title() == "Title: title_heading_content", err_msg
    # cleanup
    shutil.rmtree(notes_dir)


def test_note_construction():
    for idx, note_file in enumerate(NOTE_HTML_FILES):
        # setup
        notes_dir = Path(tempfile.mkdtemp())
        with open(note_file) as file:
            note_path = create_note_file(file.read(), notes_dir)
        note = Note(note_path)
        # check whether title is correctly constructed
        title_err_msg = f"Title is not correctly constructed for note {note_file}"
        assert note.get_title() == NOTE_TITLES[idx], title_err_msg
        # check whether headline is correctly constructed
        headline_err_msg = f"Headline is not correctly constructed for note {note_file}"
        assert note.get_headline() == NOTE_HEADLINES[idx], headline_err_msg
        # check whether the sections are correctly constructed
        sections_err_msg = f"Sections are not correctly constructed for note {note_file}"
        assert len(note.get_sections()) == NOTE_SECTION_CNTS[idx], sections_err_msg
        # cleanup
        shutil.rmtree(notes_dir)


if __name__ == "__main__":

    # given a correct html input, nbx.note's api should:
    # extract the correct corresponding content
    test_note_construction()

    # given a specific operation on a note, nbx.note's api should:
    # apply the desired changes and reflect the changes to disk
    test_note_update_body()
    test_note_update_title()
    test_note_save()
    test_note_mulitple_save()
    test_note_reset()
    test_note_archive()
