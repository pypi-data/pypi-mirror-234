import re
from collections import abc, deque
from typing import NamedTuple, Self

from .patterns import categorize_header


class Block(NamedTuple):
    """Each opinion, especially the main opinion, can be subdivided into blocks of text.

    A `body` of text passed can be broken down further into `@children` blocks. The division is
    based on semi-automated markdown headers that can be manually fixed. The rationale for is to
    create better text segmentation for embeddings. This assumes that the `body` of text contains
    a `heading_level` starting with 2, e.g. 2 `#` characters, but may contain nested blocks within:

    ```markdown
    ## Sample heading 1

    A paragraph

    ### Another heading underneath 1

    ## Sample heading 2

    > hello world
    ```

    The `material_path` starts with "1." and all child blocks will inherit
    from this as the root path.

    The heading `title` may be:

    1. a `marker` which divides text such as roman numeral, a letter, a number, e.g. `I.`, `I.A.4`, etc.; or
    2. a `label`, akin to a chapter in a book, e.g. `Ruling of the Court`, `Issues`, `Antecedent Facts`, etc. or
    3. a `phrase`, akin to a section inside a chapter, e.g. `There is not enough evidence to... xxx`

    """  # noqa: E501

    material_path: str = "1."
    heading_level: int = 2
    inherited_category: str | None = None
    title: str | None = None
    body: str = ""
    order: int | None = None

    def __repr__(self) -> str:
        if self.title:
            return f"<Block {self.material_path}: {self.title}>"
        return f"<Block {self.material_path}>"

    @property
    def heading_regex(self):
        """Uses explicit number of `#` characters for regex pattern creation."""
        return rf"^#{ {self.heading_level} }\s"

    @property
    def divider(self) -> re.Pattern:
        """Pattern to split `body` into `@children`; uses `\\n` prior to the `@heading_regex`."""  # noqa: E501
        return re.compile(rf"\n(?={self.heading_regex})", re.M)

    def get_heading_text(self, text: str) -> str | None:
        """Uses pattern to extract `title` of each block yield from `@children`."""
        if match := re.search(rf"(?<={self.heading_regex}).*", text):
            return match.group().strip()
        return None

    def get_body_text(self, text: str) -> str:
        """Uses pattern to extract `body` of each block yield from `@children`."""
        return re.sub(rf"{self.heading_regex}.*", "", text).strip()

    def get_children(self):
        """Each `body` may be split into component sub-blocks.

        The splitter should result in at least two parts; if the body isn't split
        then no children blocks result.
        """
        children = list(self.divider.split(self.body))
        if len(children) == 1:
            return None

        head_cat = categorize_header(self.title) if self.title else None
        for counter, subcontent in enumerate(children, start=1):
            subtitle = None
            subcat = None
            if subtitle := self.get_heading_text(subcontent):
                subcat = categorize_header(subtitle)
            yield Block(
                material_path=self.material_path + f"{counter}.",
                heading_level=self.heading_level + 1,
                inherited_category=head_cat or self.inherited_category or subcat,
                title=subtitle,
                body=self.get_body_text(subcontent),
            )

    def get_blocks(self) -> abc.Iterator[Self]:
        """Recursive function to get all blocks, with each
        block getting its own nested children."""
        yield self

        children = list(self.get_children())
        if not children:
            return
        q = deque(children)

        while True:
            try:
                blk = q.popleft()
            except IndexError:
                break
            yield from blk.get_blocks()

    @property
    def blocks(self):
        blks = list(self.get_blocks())
        if len(blks) != 1:
            for cnt, blk in enumerate(blks[1:]):
                data = blk._asdict()
                data["order"] = cnt
                yield Block(**data)
