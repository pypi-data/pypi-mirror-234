import os
from typing import List
from nbx.note import Note, Record

from rich.text import Text
from rich.console import group

from nbx import util

SEARCH_RESULT_TITLE_TEXT_MAX_LENGTH_PERCENTAGE = 0.9
TITLE_TEXT_MAX_LENGTH_PERCENTAGE = 0.8
TAGS_STRING_TEXT_MAX_LENGTH_PERCENTAGE = 0.15


@group()
def get_log_content(logs: List[str]) -> Text:
    for log in logs:
        yield log


@group()
def get_panel_records(records: List[Record], notes: List[Note]) -> Text:
    terminal_width = os.get_terminal_size().columns
    for idx, (record, note) in reversed(list(enumerate(zip(records, notes)))):
        title = note.get_title().strip()
        heading = record.heading.strip()
        content = record.content.strip()
        # truncage content if it takes more than 3 lines
        lines = content.split("\n")
        if len(lines) > 3:
            content = "\n".join(lines[:3])
        if len(content) > terminal_width * 2:
            content = content[:terminal_width * 2]
        # note title or headline
        styled_title = f"[[blue]{idx}[/blue]]" + " " * \
            (len(str(len(notes))) - len(str(idx)) + 1)
        if title:
            styled_title += f"[dim cyan]{title.strip()}[/dim cyan] " + "[blue]❯ [/blue]"
        if heading:
            styled_title += f"{heading}"
        else:
            styled_title += f"{content}"
        record_text = Text.from_markup(styled_title)
        record_text.truncate(
            int(terminal_width * SEARCH_RESULT_TITLE_TEXT_MAX_LENGTH_PERCENTAGE),
            overflow="ellipsis"
        )
        if content:
            record_text.append_text(Text.from_markup(f"\n[dim]{content}[/dim]"))
        yield record_text


@group()
def get_panel_notes(notes: List[Note]) -> Text:
    PADDING_MAGIC_NUM = 4
    terminal_width = os.get_terminal_size().columns
    for idx, note in reversed(list(enumerate(notes))):
        title = note.get_title()
        headline = note.get_headline()
        # note title or headline
        styled_title = f"[[blue]{idx}[/blue]]" + " " * \
            (len(str(len(notes))) - len(str(idx)) + 1)
        if not title == "":
            styled_title += title
        else:
            styled_title += f"[dim white]{headline}[/dim white]"
        title_text = Text.from_markup(styled_title)
        # note tags
        tags = note.get_tags()
        tags_str = ""
        for tag in tags:
            tags_str += fr" [{tag}]"
        tags_text = Text.from_markup(f"[dim white]{tags_str}[/dim white]")
        # format note title & tags texts
        title_text.truncate(
            int(terminal_width * TITLE_TEXT_MAX_LENGTH_PERCENTAGE), overflow="ellipsis")
        tags_text.truncate(
            int(terminal_width * TAGS_STRING_TEXT_MAX_LENGTH_PERCENTAGE), overflow="ellipsis")
        magic_num = PADDING_MAGIC_NUM
        if util.lang_detect(title_text.plain) == "zh":
            zh_char_cnt = util.count_zh_char(title_text.plain)
            magic_num = PADDING_MAGIC_NUM + zh_char_cnt
        white_space_cnt = terminal_width - title_text._length - \
            tags_text._length - magic_num
        content_text = title_text
        content_text.pad_right(white_space_cnt)
        content_text.append_text(tags_text)
        yield content_text


def get_panel_title(tags: List[str] = [], selected_tag_idxs: List[int] = []) -> str:
    title_str = "Saved Query: " if len(tags) > 0 else ""
    markup_start = "[u blue]"
    markup_end = "[/u blue]"
    separator = "[dim white]·[/dim white]"
    for idx, tag in enumerate(tags):
        # captialize each word in tag to avoid confusion with styling text
        tag = f"[{tag if tag[0].isupper() else tag.title()}]"
        if idx > 0:
            title_str += f" {separator}"
        if idx in selected_tag_idxs:
            tag = f"{markup_start}{tag}{markup_end}"
        title_str += f" {tag}"
    return title_str.strip()


def get_panel_subtitle(commands: List[str]) -> str:
    subtitle_str = "[dim white]❯[/dim white]"
    separator = "[dim blue]·[/dim blue]"
    for idx, command in enumerate(commands):
        if idx > 0:
            subtitle_str += f" {separator}"
        subtitle_str += f" [dim white]{command}[/dim white]"
    return subtitle_str.strip()


def format_headline(headline: str) -> str:
    if len(headline) > 120:
        headline = headline[:117]
        headline += "..."
    return headline
