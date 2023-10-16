import logging
import os
import pathlib
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from nbx import nbx, util, config
from nbx.note import Note

FRONTEND_SESSION_STATE = {
    # See all page options in ./frontend/src/App.svelte
    "routing": {"page": "", "params": {}},
    # EditNote related
    "relevantRecords": [],
    "uploadedImageUrl": "",
    "noteTitle": "",
    "noteContent": "",
    # EditInsight related
    "insightGraph": {"nodes": [], "edges": [], "selectedNodes": []},
    "statementHtmls": [],
    # ListNotes related
    "selectedNoteIdx": -1,
    # Connection related
    "connectedToBackend": True,
}

BACKEND_SESSION_STATE = {
    # EditNote related
    "note": None,
    "last_note_edit_timestamp": None,
    "last_relevant_search_timestamp": None,
    # ListNotes related
}

logger = logging.getLogger(__name__)

####################################################################################################
# FastAPI Configurations

HOST = "localhost"
PORT = 8000

app = FastAPI()

# Allow CORS from svelte frontend to fastapi backend
origins = [
    f"http://{HOST}",
    f"http://{HOST}:{PORT}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd = pathlib.Path(__file__).parent.resolve()
app.mount(
    "/app",
    StaticFiles(directory=Path(pwd, "frontend/dist/"), html=True),
    name="static",
)

####################################################################################################
# Logics for handling data sent by the UI frontend


def should_invoke_relevant_search(input: str):
    # if the input is too short to contain enough semantic, simply skip
    if len(input) < 15:
        return False
    # relevant search should not be called within 30 seconds after the previous call
    current_timestamp = datetime.now()
    previous_timestamp = BACKEND_SESSION_STATE["last_relevant_search_timestamp"]
    if previous_timestamp:
        previous_timestamp = datetime.strptime(previous_timestamp, "%Y-%m-%d-%H-%M-%S")
        if (current_timestamp - previous_timestamp).total_seconds() < 30:
            return False
    return True


def handle_save_note():
    global BACKEND_SESSION_STATE
    note = BACKEND_SESSION_STATE["note"]
    has_changed = True
    if note:
        has_changed = note.has_changed
        note.save()
    else:
        full_content = FRONTEND_SESSION_STATE["noteContent"]
        if FRONTEND_SESSION_STATE["noteTitle"] != "<h1></h1>":
            full_content = FRONTEND_SESSION_STATE["noteTitle"] + "\n" + full_content
        note_file_path = nbx.create_note(full_content)
        BACKEND_SESSION_STATE["note"] = Note(note_file_path)
    if has_changed:
        nbx.index_all_notes(background=True)


def handle_exit():
    note = BACKEND_SESSION_STATE["note"]
    if note:
        note.reset()
    util.terminate_process()


def handle_update_note(data):
    global FRONTEND_SESSION_STATE
    global BACKEND_SESSION_STATE
    if "data" not in data:
        logger.warning("Invalid update_note websocket: No data specified", data)
        return

    input = data["data"]["input"]
    content = data["data"]["content"]
    update_type = data["data"]["updateType"]
    if update_type == "noteContent":
        FRONTEND_SESSION_STATE["noteContent"] = content
    if update_type == "noteTitle":
        FRONTEND_SESSION_STATE["noteTitle"] = content

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    BACKEND_SESSION_STATE["last_note_edit_timestamp"] = timestamp
    note = BACKEND_SESSION_STATE["note"]
    if note:
        if update_type == "noteContent":
            note.update_body(content)
        if update_type == "noteTitle":
            note.update_title(content)
    # find relevant note abstracts as prompts for the user to select
    # note: this is a blocking call and will take a while, shouldn't be called too often
    print(f"[Current User Input] {input}")
    if should_invoke_relevant_search(input):
        print(f"[Relevant Notes Search] {input}")
        BACKEND_SESSION_STATE["last_relevant_search_timestamp"] = timestamp
        relevantRecords = nbx.find_relevant_records(input)
        FRONTEND_SESSION_STATE["relevantRecords"] = relevantRecords


def handle_show_note(data):
    global FRONTEND_SESSION_STATE
    if "data" not in data:
        logger.warning("Invalid update_note websocket: No data specified", data)
        return

    filename = data["data"]["filename"]
    nbx_config = config.load_config()
    note = Note(Path(nbx_config.get("notes_dir"), filename))
    note_title = "<h1>" + note.get_title() + "</h1>"  # get_title returns pure text without h1 tag
    note_content = note.get_body()
    FRONTEND_SESSION_STATE["routing"]["params"] = {
        "noteTitle": note_title,
        "noteContent": note_content,
        "logs": note.logs,
        "filename": filename,
    }
    FRONTEND_SESSION_STATE["noteTitle"] = note_title
    FRONTEND_SESSION_STATE["noteContent"] = note_content
    BACKEND_SESSION_STATE["note"] = note


def handle_upload_image(data):
    global FRONTEND_SESSION_STATE

    if "data" not in data:
        logger.warning("Invalid upload_image websocket: No data specified", data)
        return
    image = data["data"]["image"]
    image_name = nbx.add_image(image)
    FRONTEND_SESSION_STATE[
        "uploadedImageUrl"
    ] = f"http://{HOST}:{PORT}/images/{image_name}"


def handle_data(data):
    if "type" not in data:
        logger.warning("Invalid websocket data: No type specified", data)
        return
    data_type = data["type"]

    if data_type == "exit":
        handle_exit()
    elif data_type == "save_note":
        handle_save_note()
    elif data_type == "update_note":
        handle_update_note(data)
    elif data_type == "upload_image":
        handle_upload_image(data)
    elif data_type == "show_note":
        handle_show_note(data)


####################################################################################################
# FastAPI Endpoints


@app.get("/images/{filename}")
async def images(filename: str) -> FileResponse:
    image_path = nbx.get_image_path(filename)
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Item not found")
    return FileResponse(image_path)


@app.get("/data")
async def data():
    return FRONTEND_SESSION_STATE


@app.websocket("/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            handle_data(data)
            await websocket.send_json(FRONTEND_SESSION_STATE)
    except WebSocketDisconnect:
        logger.info("connection closed")


@app.get("/")
async def root():
    return RedirectResponse(url="app")


@app.on_event("startup")
async def startup_event():
    webbrowser.open_new(f"http://{HOST}:{PORT}")


def add_note(host: str = HOST, port: int = PORT) -> None:
    global FRONTEND_SESSION_STATE
    FRONTEND_SESSION_STATE["routing"] = {"page": "EditNote", "params": {}}
    uvicorn.run(app, host=host, port=port)


def edit_note(
    note: Note, host: str = HOST, port: int = PORT, read_only: bool = False
) -> None:
    global FRONTEND_SESSION_STATE
    global BACKEND_SESSION_STATE
    note_title = "<h1>" + note.get_title() + "</h1>"  # get_title returns pure text without h1 tag
    note_content = note.get_body()
    # @TODO This param is a redundant info as it is only needed to initialize UI components
    # And also the info is already recorded in the FRONTEND_SESSION_STATE
    add_note_params = {
        "noteTitle": note_title,
        "noteContent": note_content,
        "logs": note.logs,
        "filename": os.path.basename(note.file),
    }
    FRONTEND_SESSION_STATE["routing"] = {"page": "EditNote", "params": add_note_params}
    FRONTEND_SESSION_STATE["connectedToBackend"] = not read_only
    FRONTEND_SESSION_STATE["noteTitle"] = note_title
    FRONTEND_SESSION_STATE["noteContent"] = note_content
    BACKEND_SESSION_STATE["note"] = note
    uvicorn.run(app, host=host, port=port)


def list_notes(
    note_infos: List[Dict[str, Any]], host: str = HOST, port: int = PORT
) -> None:
    global FRONTEND_SESSION_STATE
    FRONTEND_SESSION_STATE["routing"] = {
        "page": "ListNotes",
        "params": {"noteInfos": note_infos},
    }
    uvicorn.run(app, host=host, port=port)
