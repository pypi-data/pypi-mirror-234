from __future__ import annotations

from pathlib import Path
from typing import Any

def _parse_flat_file_to_dict(
    xml_file: str | Path, short_names: bool
) -> dict[str, list[dict[str, Any]]]: ...
def _parse_flat_file_to_pandas_dict(
    xml_file: str | Path, short_names: bool
) -> dict[str, list[Any]]: ...

class FileNotFoundError(Exception):
    pass

class InvalidFileTypeError(Exception):
    pass

class ParsingError(Exception):
    pass
