from typing import List, Set
from pathlib import Path
from urllib.request import urlopen, Request
from .constants import PROVIDER_URL


def get_templates(url: str = PROVIDER_URL) -> List[str]:
    output: List[str] = []
    with urlopen(Request(url + "list", headers={"User-Agent": "Python"})) as request:
        response: str = request.read().decode("utf-8")
        for line in response.splitlines():
            output.extend(line.split(","))
    return output


def download_gitignore(filename: Path, template: Set[str], url: str = PROVIDER_URL) -> None:
    with urlopen(Request(url + ",".join(sorted(template)), headers={"User-Agent": "Python"})) as request:
        with open(filename, mode="wb") as file:
            file.write(request.read())
