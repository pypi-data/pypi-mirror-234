from typing import List
from itertools import chain
from ..constants import PROVIDER_URL
from ..provider import get_templates


def find(term: str, url: str = PROVIDER_URL) -> None:
    term = term.lower()
    starts: List[str] = []
    contains: List[str] = []
    print(f"Searching term: {term}\n")
    for name in get_templates(url):
        lower = name.lower()
        if lower.startswith(term):
            starts.append(name)
        elif term in lower:
            contains.append(name)

    if len(starts) == 0 and len(contains) == 0:
        print("Nothing found.")
        return
    for name in chain(starts, contains):
        print(name)
