import os
import shutil
from abc import ABC
from datetime import datetime
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup

from nbx.util import save_json_obj, load_json


class Record(ABC):
    def __init__(
        self,
        id: str,
        heading: str,
        headingType: str,
        headingIdx: int,
        content: str,
        filename: str,
    ) -> None:
        super().__init__()
        self.id = id
        self.heading = heading
        # heading's corresponding html tag type
        self.headingType = headingType
        # heading index based on its headingType
        self.headingIdx = headingIdx
        self.content = content
        self.filename = filename


class Note(ABC):

    def __init__(self, file: Path, cache: bool = True) -> None:
        super().__init__()
        self.file = file
        self.logs = {}
        self.last_update = ""
        self.html = ""
        self.alias = ""
        self.notes_dir = os.path.dirname(file)
        self.has_changed = False
        self._load_file(file, cache)

    def _load_file(self, note_file: Path, cache: bool) -> None:
        # load the main note
        note = load_json(note_file)
        self.logs = note["content"]
        self.last_update = note["lastUpdate"]
        self.html = self.logs[self.last_update]
        self.alias = note.get("alias", "")
        # load the temporary note if exist
        tmp_note_file = Path(os.path.dirname(note_file), ".tmp", f"{self.last_update}.html")
        if tmp_note_file.exists() and cache:
            self.has_changed = True
            with open(tmp_note_file) as tmp_note_file:
                self.html = tmp_note_file.read()

    def _save_tmp_note(self):
        tmp_notes_dir = Path(self.notes_dir, ".tmp")
        if not tmp_notes_dir.exists():
            tmp_notes_dir.mkdir(parents=True)
        tmp_note_file_path = Path(tmp_notes_dir, f"{self.last_update}.html")
        with open(tmp_note_file_path, "w+") as tmp_note_file:
            tmp_note_file.write(self.html)

    def save(self) -> None:
        if not self.has_changed:
            return
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        last_update = self.last_update
        self.last_update = timestamp
        self.logs[timestamp] = self.html
        # remove old note
        old_note = Path(self.notes_dir, f"{last_update}.json")
        if old_note.exists():
            os.remove(old_note)
        # save the note to disk
        note_json = {"lastUpdate": timestamp, "content": self.logs, "alias": self.alias}
        note_file = Path(self.notes_dir, f"{timestamp}.json")
        save_json_obj(note_file, note_json)
        self.file = note_file
        # remove tmporary note
        tmp_note_file = Path(self.notes_dir, ".tmp", f"{last_update}.html")
        if tmp_note_file.exists():
            os.remove(tmp_note_file)
        self.has_changed = False

    def archive(self) -> None:
        archive_notes_dir = Path(self.notes_dir, "archive")
        archive_notes_dir.mkdir(parents=True, exist_ok=True)
        src_path = Path(self.notes_dir, f"{self.last_update}.json")
        dst_path = Path(archive_notes_dir, f"{self.last_update}.json")
        shutil.move(src_path, dst_path)

    def reset(self) -> None:
        self.html = self.logs[self.last_update]
        # remove temporary note
        tmp_note_file = Path(self.notes_dir, ".tmp", f"{self.last_update}.html")
        if tmp_note_file.exists():
            os.remove(tmp_note_file)

    def update_title(self, title: str) -> None:
        self.has_changed = True
        doc = BeautifulSoup(self.html, features="html.parser")
        components = doc.find_all(recursive=False)
        # remove the old title if exist
        if len(components) > 0 and components[0].name == "h1":
            components[0].decompose()
        # add the new title
        if title:
            if "<h1>" in title:
                title_component = BeautifulSoup(title, features="html.parser")
            else:
                title_component = BeautifulSoup(f"<h1>{title}</h1>", features="html.parser")
            # add title if it is not empty
            if title_component.text.strip():
                doc.insert(0, title_component)
        self.html = doc.prettify()
        self._save_tmp_note()

    def update_body(self, body_html: str) -> None:
        self.has_changed = True
        doc = BeautifulSoup(self.html, features="html.parser")
        components = doc.find_all(recursive=False)
        body_component = BeautifulSoup(body_html, features="html.parser")
        # if the doc contains a title
        if len(components) > 0 and components[0].name == "h1":
            title_component = components[0]
            body_component.insert(0, title_component)
        self.html = body_component.prettify()
        self._save_tmp_note()

    def update_alias(self, alias: str) -> None:
        self.has_changed = True
        self.alias = alias

    def get_headline(self) -> str:
        note_content = BeautifulSoup(self.html, features="html.parser")
        components = note_content.find_all(recursive=False)
        if len(components) == 0:
            return ""
        return components[0].text.strip()

    def get_title(self) -> str:
        note_content = BeautifulSoup(self.html, features="html.parser")
        if note_content.find("h1"):
            return note_content.find("h1").text.strip()
        return ""

    def get_body(self) -> str:
        note_content = BeautifulSoup(self.html, features="html.parser")
        components = note_content.find_all(recursive=False)
        if len(components) == 0:
            return ""
        if components[0].name == "h1":  # A note starts with a H1 heading
            components[0].decompose()
            return note_content.prettify()
        return self.html

    def get_tags(self) -> List[str]:
        return [self.last_update[:10]]  # Date like [2022-02-22] as the default tag

    def get_sections(self) -> List[Record]:
        heading_index_map = {"h1": 0, "h2": 0, "p": 0}
        note_content = BeautifulSoup(self.html, features="html.parser")
        components = note_content.find_all(recursive=False)
        if len(components) == 0:
            return []
        # Extract records from the note
        records = []
        if components[0].name == "h1":  # A note starts with a H1 heading
            heading = components[0].text.strip()
            components = components[1:]
            content = heading  # If the h1 heading has no content, then use the heading
            if len(components) > 0 and components[0].name == "p":
                content = components[0].text.strip()
                components = components[1:]
                heading_index_map["p"] = heading_index_map.get("p") + 1
            record = Record(
                f"{self.last_update}#{len(records)}",
                heading=heading,
                headingType="h1",
                headingIdx=heading_index_map.get("h1"),
                content=content,
                filename=os.path.basename(self.file),
            )
            heading_index_map["h1"] = heading_index_map.get("h1") + 1
            records.append(record)
        elif components[0].name != "h2":  # A note starts with a content, i.e. not section heading
            content = components[0].text.strip()
            components = components[1:]
            record = Record(
                f"{self.last_update}#{len(records)}",
                heading=content,
                headingType="p",
                headingIdx=heading_index_map.get("p"),
                content=content,
                filename=os.path.basename(self.file),
            )
            heading_index_map["p"] = heading_index_map.get("p") + 1
            records.append(record)
        # Main body of the note: <h2>heading</h2><p>content</p>
        idx = 0
        record_heading = ""
        record_content = ""
        while len(components) > 0:
            component = components[0]
            components = components[1:]
            if component.name == "h2":
                if idx != 0:  # save previous reocrd
                    record = Record(
                        f"{self.last_update}#{len(records)}",
                        heading=record_heading.strip(),
                        headingType="h2",
                        headingIdx=heading_index_map.get("h2"),
                        content=record_content.strip(),
                        filename=os.path.basename(self.file),
                    )
                    records.append(record)
                    heading_index_map["h2"] = heading_index_map.get("h2") + 1
                record_heading = component.text.strip()
                record_content = ""
                idx += 1
            else:
                content = component.text.strip()
                record_content += content + "\n"
        if record_heading:
            record = Record(
                f"{self.last_update}#{len(records)}",
                heading=record_heading,
                headingType="h2",
                headingIdx=heading_index_map.get("h2"),
                content=record_content,
                filename=os.path.basename(self.file),
            )
            records.append(record)
            heading_index_map["h2"] = heading_index_map.get("h2") + 1
        return records


def create_note_file(note_html: str, notes_dir: Path, note_filename: str = "") -> Path:
    notes_dir = Path(notes_dir)
    if not notes_dir.exists():
        notes_dir.mkdir(parents=True)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    if not note_filename:
        note_filename = timestamp
    note_file_path = Path(notes_dir, f"{note_filename}.json")
    save_json_obj(note_file_path, {
        "lastUpdate": timestamp,
        "content": {
            timestamp: note_html
        }
    })
    return note_file_path
