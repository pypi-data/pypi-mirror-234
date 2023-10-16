import json
from typing import Union
from pathlib import Path
import pkgutil

STATIC_DIR = "static"


# ensure path
def ensure_path(fp: Union[str, Path]):
    return Path(fp)


# read file
def read(fn: Path, version: str = "default"):
    fp = Path(STATIC_DIR) / f"{fn}.{version}"
    content = pkgutil.get_data(__name__, fp.as_posix()).decode()
    return content


# make dir if not exist and write file
def write(dst_fp: Path, content, mode="w"):
    dst_fp = ensure_path(dst_fp)

    # make directory
    dst_fp.parent.mkdir(parents=True, exist_ok=True)

    # write file
    with open(dst_fp, mode) as fw:
        if dst_fp.suffix.lower() in ["json"]:
            json.dump(content, fw)
        else:
            fw.write(content)
