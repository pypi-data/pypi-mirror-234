# corpus-content

![Github CI](https://github.com/justmars/corpus-content/actions/workflows/main.yml/badge.svg)

Using opinion text from frontmatter-formatted markdown files, chunk the same into segments and itemize Philippine statutes, citations within the text.

```py
from corpus_content import Decision

file = next(Path().home().joinpath("corpus-decisions").glob("gr/**/2023*/main*"))
metadata = Decision.from_file(file)
meta.main_opinion.segments
meta.separate_opinions
```

## Development

See [documentation](https://justmars.github.io/corpus-content).

1. Run `poetry install`
2. Run `poetry shell`
3. Run `pytest`
