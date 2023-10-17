from typing import Iterable
import platform
import importlib.metadata


def get_entry_points(name: str) -> Iterable[importlib.metadata.EntryPoint]:
    version = platform.python_version()
    major, minor, patch = map(lambda x: int(x), version.split('.'))
    eps = importlib.metadata.entry_points()

    # Python 3.8 & 3.9 importlib.metadata.entry_points() -> dict
    if minor == 8 or minor == 9:
        if name in eps:
            return eps[name]

    # Python 3.10+ importlib.metadata.entry_points() -> Collection
    elif minor >= 10:
        if name in eps.groups:
            return eps.select(group=name)

    return []
