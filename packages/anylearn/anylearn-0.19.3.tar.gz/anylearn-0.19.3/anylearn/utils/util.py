import os
from pathlib import Path
from typing import Union

from anylearn.utils.errors import AnyLearnException


def ensure_dir(dir_: Union[os.PathLike, str]):
    root_dir = Path(dir_)
    if root_dir.exists() and root_dir.is_file():
        raise AnyLearnException(
            f"Path `{str(dir_)}` is expected to be a directory, "
            "a file given"
        )
    root_dir.mkdir(parents=True, exist_ok=True)
