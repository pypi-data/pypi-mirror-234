from pathlib import Path
from typing import NamedTuple


class Authorship(NamedTuple):
    is_main: bool = True
    curiam: bool = False
    value: str | None = None

    @property
    def justice_digit(self):
        if self.value and self.value.isdigit():
            return int(self.value)
        return None

    @property
    def is_anonymous(self):
        if self.value and self.value.startswith("a"):
            return True
        return False


def get_writer_from_path(file: Path) -> Authorship:
    """Requires a frontmatter-formatted markdown file where filename is either:

    1. `main.md` - Undetected writer
    2. `main-<digit>.md` - Detected writer
    3. `main-pc.md` - Anonymous writer

    The filename suffix determines the existence of a `justice_id` and the `curiam`
    field.

    It must also be based on a certain path. The path will determine the citation
    row which is calculated from its docket subfields.

    The example file structure using this certain "docket" path:

    |- `/gr`
        |- `/1234`
            |- `/2023-01-01`
                |- main-172.md
            |- `/2023-05-05`
                |- main-172.md

    If the parent folder of such certain path contains a subdirectory `/opinion`,
    and the markdown files should follow another convention for separate
    opinions:

    1. `<digit>.md` - Identifier of writer
    2. `a-<digit>.md` - Anonymous writer

    The example file structure using the same "docket" path with opinions:

    |- `/gr`
        |- `/1234`
            |- `/2023-01-01`
                |- opinion
                    |- 194.md
                    |- 191.md
                |- main-172.md
            |- `/2023-05-05`
                |- opinion
                    |- 194.md
                |- main-172.md

    Args:
        file (Path): A filename that follows a convention.

    Returns:
        int | str | None: If an integer, implies a justice has been identified; if a string,
    """  # noqa: E501
    if file.suffix != ".md":
        raise Exception(f"{file=}; must be *.md")

    if file.parent.stem == "opinion":
        if file.stem.isdigit():
            return Authorship(is_main=False, value=file.stem)
        elif not file.stem.startswith("a"):
            raise Exception(f"{file=}; must either be digit or anonymous.")
        return Authorship(is_main=False, value=file.stem)

    if not file.stem.startswith("main"):
        raise Exception(f"{file=} must either be main, main-1, main-pc")
    elif file.name == "main.md":
        return Authorship(is_main=True)

    _bits = file.stem.split("-")
    if len(_bits) == 2:
        if _bits[1].isdigit():
            return Authorship(is_main=True, value=_bits[1])  # ponencia
        elif _bits[1] == "pc":
            return Authorship(is_main=True, curiam=True)  # per curiam
    raise Exception(f"Improper {file=}, could not determine id based on convention")
