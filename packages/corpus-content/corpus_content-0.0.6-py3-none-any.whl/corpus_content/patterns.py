import re
from enum import Enum


def jx(regexes: list[str], border: str = r"\s+", enclose: bool = False) -> str:
    """Joins regex strings (i.e. `regexes`) using a `border`.

    Args:
        regexes (list[str]): Raw regex strings to be joined
        border (str, optional): A regex string to be set in between `regexes`. Defaults to \r"\\s+".
        enclose (bool, optional): Whether each regex string joined should have a wrapping parenthesis `(<regex-string>)`. Defaults to False.

    Returns:
        str: A raw regex string for pattern matching.
    """  # noqa: E501
    if enclose:
        regexes = [rf"({reg})" for reg in regexes]
    return border.join(regexes)


class Phrase(Enum):
    intro = [
        [
            r"(The\s+)?(Statement|Facts|Antecedents|Antecedent\s+Facts)",
            r"of",
            r"the",
            r"Case",
        ],
        [
            r"(The\s+)?(Antecedent|Case|Fact|Antecedent\s+Fact|Background Fact|Statement\s+of\s+Facts)s?"  # noqa: E501
        ],
        [r"(The\s+)?(Relevant|Factual|Case)?", r"(Antecedents|Background)"],
        [r"The", r"Facts", r"and", r"Antecedent\s+Proceedings"],
        [r"The", r"Case", "and", r"the", r"Facts"],
    ]
    issue = [
        [r"(The\s+)?Issues?", r"Before", r"the", r"Court"],
        [r"Issues?", r"of", r"the", r"Case"],
        [r"Issues?", r"and", r"Arguments"],
        [r"(The\s+)?(Question|Issue)s?", r"Presented"],
        [r"Assignments?", r"of", r"Errors?"],
        [r"(The|Threshold|Core)", r"Issues?"],
        [r"Issues?"],
    ]
    ruling = [
        [r"(The\s+)?Ruling", r"of", r"t(his|he)", r"Court"],
        [r"T(he|his)", r"Court[',’]s", r"Rulings?"],
        [r"Our", r"Ruling"],
        [r"(Ruling|Discussion)"],
    ]

    @property
    def regex(self):
        """Each member pattern consists of a list of strings. Each string
        will be joined as an option to create the full regex string for
        each member."""
        return jx(
            regexes=[rf"{jx(regex)}(\s*\[\^\d+\])?" for regex in self.value],
            border="|",
            enclose=True,
        )

    @classmethod
    def compiler(cls) -> re.Pattern[str]:
        """Using the full regex string for each member, create named patterns
        using the member name. This ought to be compiled only once so that
        it need not create patterns every single time."""
        return re.compile(
            jx(
                regexes=[rf"(?P<{member.name}>{member.regex})" for member in cls],
                border="|",
                enclose=True,
            ),
            re.I,
        )


headers = Phrase.compiler()


def categorize_header(text: str):
    if text := text.strip():
        if match := headers.fullmatch(text):
            for k, v in match.groupdict().items():
                if v:
                    return k
