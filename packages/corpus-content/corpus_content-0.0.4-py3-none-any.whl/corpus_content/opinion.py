import re
from io import StringIO
from typing import NamedTuple

from citation_utils import CountedCitation
from markdown import Markdown  # type: ignore
from statute_utils import CountedStatute

footnote_pattern = re.compile(r"\[\^\d+\]")

two_or_more_spaces = re.compile(r"\s{2,}")


def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = unmark_element  # type: ignore
__md = Markdown(output_format="plain")  # type: ignore
__md.stripTopLevelTags = False  # type: ignore


def clear_markdown(value: str) -> str:
    """Given markdown text, strip markdown elements to get the raw text.

    1. Uses part of the code described in https://stackoverflow.com/a/54923798/9081369
    2. Will remove footnotes

    Examples:
        >>> from pathlib import Path
        >>> clear_markdown(Path(__file__).parent.parent.joinpath("tests/test.md").read_text())
        'Heading Some paragraph Another Heading Another paragraph An enumeration: First Second Third A listing hello world this A footnote'

    Args:
        value (str): markdown-based text

    Returns:
        str: Raw text without markdown
    """  # noqa: E501
    unmarked = __md.convert(value)
    result = footnote_pattern.sub("", unmarked)
    result = two_or_more_spaces.sub(" ", result)
    return result


def text_to_chunks(s, maxlength: int = 800):
    start = 0
    end = 0
    while start + maxlength < len(s) and end != -1:
        end = s.rfind(". ", start, start + maxlength + 2)
        if end == -1:
            break
        yield s[start:end]
        start = end + 1
    yield s[start:]


class Opinion(NamedTuple):
    """Whether the opinion is the main opinion of the decision
    or a separate one, it will contain common fields and associated
    records based on the content.
    """

    id: str
    decision_id: str
    content: str
    justice_id: int | None = None
    is_main: bool = True
    label: str = "Opinion"
    file_statutes: str | None = None
    file_citations: str | None = None

    def __repr__(self) -> str:
        return f"<Opinion {self.id}>"

    @property
    def base_meta(self):
        return {"opinion_id": self.id, "decision_id": self.decision_id}

    @property
    def index(self):
        try:
            return self.content.index("[^1]:")
        except ValueError:
            return None

    @property
    def body(self) -> str:
        return self.content[: self.index] if self.index else self.content

    @property
    def lines(self) -> list[str]:
        res = []
        for line in self.body.splitlines():
            if cleaned := line.strip():
                if cleared := clear_markdown(cleaned):
                    res.append(cleared)
        return res

    @property
    def segments(self):
        res = []
        if self.lines:
            for y0, line in enumerate(self.lines, start=1):
                row = {
                    "id": f"{self.id}-{str(y0)}",
                    "order": y0,
                    "text": line,
                    "char_count": len(line),
                }
                res.append(self.base_meta | row)
        return res

    @property
    def statutes(self):
        res = []
        if self.file_statutes:
            objs = CountedStatute.from_repr_format(self.file_statutes.split("; "))
            for obj in objs:
                res.append(
                    self.base_meta
                    | {
                        "cat": obj.cat,
                        "num": obj.num,
                        "mentions": obj.mentions,
                    }
                )
        return res

    @property
    def citations(self):
        res = []
        if self.file_citations:
            objs = CountedCitation.from_repr_format(self.file_citations.split("; "))
            for obj in objs:
                res.append(self.base_meta | obj.model_dump())
        return res
