import base64
import glob
import json
import os
import pathlib
import psutil
import re
from typing import Any, Dict
from pathlib import Path


def load_json(file_path: pathlib.Path) -> Dict:
    with open(file_path, "r") as file:
        try:
            json_obj = json.load(file)
            return json_obj
        except json.JSONDecodeError as e:
            if os.stat(file_path).st_size == 0:
                # Empty file
                return {}
            else:
                raise e


def save_json_obj(file_path: pathlib.Path, json_obj: Dict) -> None:
    with open(file_path, "w+") as json_file:
        json.dump(json_obj, json_file, sort_keys=True)
        json_file.flush()


def set_json_value(file_path: pathlib.Path, key: str, value: Any) -> None:
    # key needs to follow python naming convention, such as trial_id
    config = {}
    if file_path.exists():
        with open(file_path, "r") as json_file:
            try:
                config = json.load(json_file)
            except json.JSONDecodeError as e:
                if os.stat(file_path).st_size == 0:
                    # Empty file
                    config = {}
                else:
                    raise e
    config[key] = value
    with open(file_path, "w+") as json_file:
        json.dump(config, json_file)
        json_file.flush()


def load_json_value(file_path: pathlib.Path, key: str, default_value: Any = "") -> Any:
    with open(file_path, "r") as json_file:
        try:
            config = json.load(json_file)
        except json.JSONDecodeError as e:
            if os.stat(file_path).st_size == 0:
                # Empty file
                return default_value
            else:
                raise e
        if key not in config:
            return None
        return config[key]


def terminate_process():
    current_process = psutil.Process(os.getpid())
    current_process.terminate()


def verify_openai_token(token: str) -> str:
    import openai
    openai.api_key = token
    try:
        openai.Completion.create(
            model="text-ada-001",
            prompt="Hello",
            temperature=0,
            max_tokens=10,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0
        )
        return "OK"
    except Exception as e:
        return str(e)


def save_base64(img_data, file_path: pathlib.Path):
    with open(file_path, "wb") as fh:
        fh.write(base64.decodebytes(bytes(img_data, encoding="utf-8")))


def lang_detect(text: str):
    # # korean
    # if re.search("[\uac00-\ud7a3]", texts):
    #     return "ko"
    # # japanese
    # if re.search("[\u3040-\u30ff]", texts):
    #     return "ja"
    # chinese
    if re.search("[\u4e00-\u9FFF]", text):
        return "zh"
    return None


def count_zh_char(text: str) -> int:
    res = len(re.findall("[\u4e00-\u9FFF]", text))
    res += len(re.findall("，", text))
    res += len(re.findall("。", text))
    res += len(re.findall("：", text))
    res += len(re.findall("？", text))
    return res


def clean_folder(folder: Path):
    files = glob.glob(f"{os.fspath(folder)}/*")
    for f in files:
        os.remove(f)
