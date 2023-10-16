from typing import List, Generator
from ..constants import PROVIDER_URL, GITIGNORE_FILENAME
from .update import update
from .template import current


def add_template(templates: List[str], url: str = PROVIDER_URL) -> None:
    update(current().union(_to_lower(templates)), url)


def remove_template(templates: List[str], url: str = PROVIDER_URL) -> None:
    update(current().difference(_to_lower(templates)), url)


def list_gitignore() -> None:
    for template in sorted(current()):
        print(template)


def create_gitignore(templates: List[str], url: str = PROVIDER_URL) -> None:
    with open(GITIGNORE_FILENAME, mode="wb"):
        pass
    update(set(_to_lower(templates)), url)


def update_gitignore(url: str = PROVIDER_URL) -> None:
    update(current(), url)


def _to_lower(items: List[str]) -> Generator[str, None, None]:
    for item in items:
        yield item.lower()
