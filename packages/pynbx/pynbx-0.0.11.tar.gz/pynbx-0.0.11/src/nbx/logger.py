import logging
from pathlib import Path


def init():
    log_dir = Path(Path.home(), ".nbx")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = Path(log_dir, "nbx.log")
    log_file.touch(exist_ok=True)

    logging.basicConfig(
        filename=log_file,
        level=logging.WARNING,
        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
