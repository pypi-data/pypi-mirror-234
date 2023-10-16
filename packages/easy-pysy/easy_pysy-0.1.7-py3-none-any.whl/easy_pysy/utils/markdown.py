import csv
from typing import Iterable, Callable, Any


def read_md_table(lines: Iterable[str], types: dict[str, Callable[[str], Any]] = None) -> Iterable[dict]:
    # Cleanup: Remove leading and trailing '|'
    lines = map(lambda line: line.lstrip('|').rstrip('|\n'), lines)

    # We use the builtin csv reader
    reader = csv.DictReader(lines, delimiter='|', quoting=csv.QUOTE_NONE)

    # Remove first header line "-----"
    next(reader)

    # Cleanup dicts (strip keys and values)
    items = map(lambda obj: _cleanup(obj), reader)

    # Post Processing
    if types:
        items = map(lambda obj: _post_process(obj, types), items)

    return items


def _post_process(obj: dict, types: dict[str, Callable[[str], Any]]):
    for key, t in types.items():
        obj[key] = t(obj[key]) if obj[key] != '' else None
    return obj


def _cleanup(obj: dict):
    return {key.strip(): value.strip() for key, value in obj.items()}
