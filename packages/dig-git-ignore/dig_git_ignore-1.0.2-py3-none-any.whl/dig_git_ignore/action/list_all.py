from ..constants import PROVIDER_URL
from ..provider import get_templates


def list_all(url: str = PROVIDER_URL) -> None:
    first_char: str = "?"
    print("Listing all availables templates.", end="")
    for name in sorted(get_templates(url)):
        if name[0] != first_char:
            first_char = name[0]
            print(f"\n{first_char.upper()}:\n  {name}", end="")
        else:
            print(f", {name}", end="")
