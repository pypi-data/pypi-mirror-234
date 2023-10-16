# Markie

A small project for processing markdown files with metadata.

## Install

```
pip install markie
```

> Note: This project is still in Alpha – significant changes are expected and
> features are limited

## Example

```python
from pprint import pprint

from markie import Doc

main_content = """
---
title: "Ducks: And how to Make Them Pay"
year: 1894
---

# Ducks: And how to Make Them Pay

By William Cook

Author of "The Practical Poultry Breeder and Feeder";
"The Horse: its keep and management";
"Pheasants, Turkeys, and Geese: their management for pleasure and profit"
""".strip()

chapter_1 = """
## Introduction

Not so many years ago roast duck was a luxury only for the rich, unless it 
might have been a few foreign birds sent into our markets, which could 
usually be bought up at a very low price. 
""".strip()

doc = Doc.from_md(main_content)

# content can be appended with .append, or prepended with .prepend
doc.append(chapter_1)

# Metadata can be retrieved and set
doc.metadata["authors"] = ["William Cook"]

# can be pretty printed to quickly glean the overall document structure
pprint(doc)

# Iterating over docs yields markdown-it tokens in order
# pprint([*doc])

# Docs are rendered to markdown
with open(f"{doc.metadata['title']}.md", "w") as f:
    f.write(doc.render())
```

The above would print:

```text
Doc(metadata={'authors': ['William Cook'],
              'title': 'Ducks: And how to Make Them Pay',
              'year': 1894},
    preamble='',
    sections=[Section(level=1,
                      title='Ducks: And how to Make Them Pay',
                      preamble='By William Cook\n'
                               '\n'
                               'Author of "The Practical Poultry Breeder and '
                               'Feeder";\n'
                               '"The Horse: its keep and management";\n'
                               '"Pheasants, Turkeys, and Geese: their '
                               'management for pleasure and profit"',
                      subsections=[Section(level=2,
                                           title='Introduction',
                                           preamble='Not so many years ago '
                                                    'roast duck was a luxury '
                                                    'only for the rich, unless '
                                                    'it\n'
                                                    'might have been a few '
                                                    'foreign birds sent into '
                                                    'our markets, which could\n'
                                                    'usually be bought up at a '
                                                    'very low price.',
                                           subsections=[])])])
```

And write the following to a file "Ducks: And how to Make Them Pay.md":

```markdown
---
title: 'Ducks: And how to Make Them Pay'
year: 1894
authors:
  - William Cook
---

# Ducks: And how to Make Them Pay

By William Cook

Author of "The Practical Poultry Breeder and Feeder";
"The Horse: its keep and management";
"Pheasants, Turkeys, and Geese: their management for pleasure and profit"

## Introduction

Not so many years ago roast duck was a luxury only for the rich, unless it
might have been a few foreign birds sent into our markets, which could
usually be bought up at a very low price.
```

## Notes for Developers

### Tests

Install the test requirements from `tests/requirements.txt`.

These tests
use [ApprovalTests](https://github.com/approvals/ApprovalTests.Python) and
[pytest](https://docs.pytest.org/en/7.4.x/) with the
[ApprovalTests pytest plugin](https://github.com/approvals/ApprovalTests.Python.PytestPlugin).
To enable diff checking on PyCharm, see
[their documentation](https://github.com/approvals/ApprovalTests.Python.PytestPlugin#tip-for-jetbrains-toolbox-and-pycharm-users)
which describes how to set up a run configuration which uses PyCharm's built-in
diff checker.
