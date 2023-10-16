from pprint import pformat

from approvaltests import verify

from markie import Doc

PARA = "In the mind's eye one sees dinosaurs, mammoths, and sabertoothed tigers"


def test_a_paragraph_of_text_can_be_parsed():
    doc = Doc.from_md(PARA)
    assert len(doc.sections) == 0
    assert doc.metadata == {}
    verify(pformat(doc, width=120, sort_dicts=False))


def test_a_paragraph_of_text_can_be_rendered():
    doc = Doc.from_md(PARA)
    verify(doc.render())


PARA_WITH_METADATA = """
---
title: Jo Brand
src: https://en.wikipedia.org/wiki/Jo_Brand
---

Her Doc Marten boots, large size, and short hair led to false rumours 
that she was a lesbian.
""".strip()


def test_a_paragraph_of_text_with_metadata_can_be_parsed():
    doc = Doc.from_md(PARA_WITH_METADATA)
    assert len(doc.sections) == 0
    assert doc.metadata == {
        "title": "Jo Brand",
        "src": "https://en.wikipedia.org/wiki/Jo_Brand"
    }
    verify(pformat(doc, width=120, sort_dicts=False))


def test_a_paragraph_of_text_with_metadata_can_be_rendered():
    doc = Doc.from_md(PARA_WITH_METADATA)
    verify(doc.render())


def test_document_metadata_can_be_modified_and_rendered():
    doc = Doc.from_md(PARA_WITH_METADATA)
    doc.metadata["title"] += "!!!"
    doc.metadata["subtitle"] = "A biography"
    verify(doc.render())


SEC = """
# Strategies for Creative Problem Solving

The purpose of this book is to help problem solvers improve their street smarts.
"""


def test_section_can_be_parsed():
    doc = Doc.from_md(SEC)
    assert len(doc.sections) == 1
    assert len(doc.preamble) == 0
    assert doc.sections[0].title == "Strategies for Creative Problem Solving"
    assert doc.sections[0].level == 1
    assert doc.metadata == {}
    verify(pformat(doc, width=120, sort_dicts=False))


def test_section_can_be_rendered():
    doc = Doc.from_md(SEC)
    verify(doc.render())


SEC_WITH_METADATA = """
---
title: All About Envelopes
src: https://en.wikipedia.org/wiki/Windowed_envelope
---

## Envelopes

Satisfactorily-strong envelopes for business and general-purpose domestic
correspondence can be, and are, in fact, made out of paper of various qualities.
""".strip()


def test_section_with_metadata_can_be_parsed():
    doc = Doc.from_md(SEC_WITH_METADATA)
    assert doc.metadata == {
        "title": "All About Envelopes",
        "src": "https://en.wikipedia.org/wiki/Windowed_envelope"
    }
    assert len(doc.sections) == 1
    assert len(doc.preamble) == 0
    assert doc.sections[0].title == "Envelopes"
    assert doc.sections[0].level == 2
    verify(pformat(doc, width=120, sort_dicts=False))


def test_section_with_metadata_can_be_rendered():
    doc = Doc.from_md(SEC_WITH_METADATA)
    verify(doc.render())


# The Long Quiche Goodbye, Avery Aames
SEC_WITH_PRELUDE = r"""
Welcome to the grand opening of Fromagerie Bessette. Or 
as it's more commonly known by the residents of small-town Providence, 
Ohio-the Cheese Shop. Proprietor Charlotte Bessette has prepared a delightful 
sampling of bold Cabot Clothbound Cheddar, delicious tortes of Stilton and 
Mascarpone, and a taste of Sauvignon Blanc-but someone else has decided to 
make a little crime of passion the piece de resistance. Right outside the 
shop Charlotte finds a body, the victim stabbed to death with one of her 
prized olive-wood handled knives.

# Chapter 1

"I'm not dead, Charlotte," Grandpère Etienne said.\
"But you are retired, Pépère. I tweaked his rosy cheek and skirted around him 
to throw a drop cloth over the rustic wooden table that usually held wheels 
of cheese, like Abbaye de Belloc, Manchego, and Humboldt Fog, the latter 
cheese a great pairing with chardonnay. Dust billowed up as the edges of the 
drop cloth hit the shop floor.
"""


def test_section_with_preamble_can_be_parsed():
    doc = Doc.from_md(SEC_WITH_PRELUDE)
    assert len(doc.sections) == 1
    assert len(doc.preamble) != 0
    assert doc.sections[0].title == "Chapter 1"
    assert doc.sections[0].level == 1
    verify(pformat(doc, width=120, sort_dicts=False))


def test_section_with_preamble_can_be_rendered():
    doc = Doc.from_md(SEC_WITH_PRELUDE)
    verify(doc.render())


SEC_WITH_PRELUDE_AND_METADATA = """
---
title: Chromatic Fantasy
year: 1979
composer: Barbara Kolb
attributions: "text by: Howard Stern"
---

The text is divided into three parts which all interrelate.

## Part 1

The young woman at the next table is wearing a long purple dress,
and I consider inviting her to join me for lunch.
""".strip()


def test_section_with_preamble_and_metadata_can_be_parsed():
    doc = Doc.from_md(SEC_WITH_PRELUDE_AND_METADATA)
    assert doc.metadata == {
        "title": "Chromatic Fantasy",
        "year": 1979,
        "composer": "Barbara Kolb",
        "attributions": "text by: Howard Stern",
    }
    assert len(doc.sections) == 1
    assert len(doc.preamble) != 0
    assert doc.sections[0].title == "Part 1"
    assert doc.sections[0].level == 2
    verify(pformat(doc, width=120, sort_dicts=False))


def test_section_with_preamble_and_metadata_can_be_rendered():
    doc = Doc.from_md(SEC_WITH_PRELUDE_AND_METADATA)
    verify(doc.render())


MULTIPLE_SECTIONS = """
## Heading Number 1

Content for heading number 1

## Heading Number 2

Content for heading number 2
"""


def test_multiple_sections_of_the_same_level_can_be_parsed():
    doc = Doc.from_md(MULTIPLE_SECTIONS)
    assert len(doc.sections) == 2
    assert len(doc.preamble) == 0
    assert doc.sections[0].title == "Heading Number 1"
    assert doc.sections[0].level == 2
    assert doc.sections[1].title == "Heading Number 2"
    assert doc.sections[1].level == 2
    verify(pformat(doc, width=120, sort_dicts=False))


def test_multiple_sections_of_the_same_level_can_be_render():
    doc = Doc.from_md(MULTIPLE_SECTIONS)
    verify(doc.render())


NESTED_SECTIONS = """
## Heading Number 1

Content for heading number 1

### Heading 1-1

Content for heading number 1-1

### Heading 1-2

Content for heading number 1-2

## Heading Number 2

Content for heading number 2

### Heading 2-1

Content for heading number 2-1
"""


def test_nested_sections_can_be_parsed():
    doc = Doc.from_md(NESTED_SECTIONS)
    assert len(doc.sections) == 2
    assert len(doc.preamble) == 0
    assert doc.sections[0].title == "Heading Number 1"
    assert doc.sections[0].level == 2
    assert doc.sections[1].title == "Heading Number 2"
    assert doc.sections[1].level == 2
    verify(pformat(doc, width=120, sort_dicts=False))


def test_nested_sections_can_be_rendered():
    doc = Doc.from_md(NESTED_SECTIONS)
    verify(doc.render())


PARA1 = "The first line of text"
PARA2 = "The second line of text"


def test_two_paragraphs_can_be_prepended():
    doc = Doc.from_md(PARA2)
    doc.prepend(PARA1)
    assert len(doc.preamble) != 0
    assert len(doc.sections) == 0
    assert doc.metadata == {}
    verify(pformat(doc, width=120, sort_dicts=False))


def test_two_prepended_paragraphs_are_rendered_correctly():
    doc = Doc.from_md(PARA2)
    doc.prepend(PARA1)
    verify(doc.render())


def test_two_paragraphs_can_be_appended():
    doc = Doc.from_md(PARA1)
    doc.append(PARA2)
    assert len(doc.preamble) != 0
    assert len(doc.sections) == 0
    assert doc.metadata == {}
    verify(pformat(doc, width=120, sort_dicts=False))


def test_two_appended_paragraphs_are_rendered_correctly():
    doc = Doc.from_md(PARA1)
    doc.append(PARA2)
    verify(doc.render())


PARA_WITH_METADATA1 = """
---
title: The main paragraph
---

The original text
""".strip()

PARA_WITH_METADATA2 = """
---
title: The second paragraph
field1: an ignored field
---

The appended/prepended text
""".strip()


def test_two_paragraphs_with_metadata_can_be_prepended():
    doc = Doc.from_md(PARA_WITH_METADATA1)
    doc.prepend(PARA_WITH_METADATA2)
    assert len(doc.preamble) != 0
    assert len(doc.sections) == 0
    assert doc.metadata == {"title": "The main paragraph"}
    verify(pformat(doc, width=120, sort_dicts=False))


def test_two_prepended_paragraphs_with_metadata_are_rendered_correctly():
    doc = Doc.from_md(PARA_WITH_METADATA1)
    doc.prepend(PARA_WITH_METADATA2)
    verify(doc.render())


def test_two_paragraphs_with_metadata_can_be_appended():
    doc = Doc.from_md(PARA_WITH_METADATA1)
    doc.append(PARA_WITH_METADATA2)
    assert len(doc.preamble) != 0
    assert len(doc.sections) == 0
    assert doc.metadata == {"title": "The main paragraph"}
    verify(pformat(doc, width=120, sort_dicts=False))


def test_two_appended_paragraphs_with_metadata_are_rendered_correctly():
    doc = Doc.from_md(PARA_WITH_METADATA1)
    doc.append(PARA_WITH_METADATA2)
    verify(doc.render())


SEC1 = """
# First H1

First H1 section
"""

SEC2 = """
# Second H1

Second H1 section
"""


def test_two_sections_of_the_same_level_can_be_prepended():
    doc = Doc.from_md(SEC2)
    doc.prepend(SEC1)
    assert len(doc.sections) == 2
    assert len(doc.preamble) == 0
    assert doc.metadata == {}
    assert doc.sections[0].title == "First H1"
    assert doc.sections[0].level == 1
    assert doc.sections[1].title == "Second H1"
    assert doc.sections[1].level == 1
    verify(pformat(doc, width=120, sort_dicts=False))


def test_two_prepended_sections_of_the_same_level_can_be_rendered():
    doc = Doc.from_md(SEC2)
    doc.prepend(SEC1)
    verify(doc.render())


def test_two_sections_of_the_same_level_can_be_appended():
    doc = Doc.from_md(SEC1)
    doc.append(SEC2)
    assert len(doc.sections) == 2
    assert len(doc.preamble) == 0
    assert doc.metadata == {}
    assert doc.sections[0].title == "First H1"
    assert doc.sections[0].level == 1
    assert doc.sections[1].title == "Second H1"
    assert doc.sections[1].level == 1
    verify(pformat(doc, width=120, sort_dicts=False))


def test_two_appended_sections_of_the_same_level_can_be_rendered():
    doc = Doc.from_md(SEC1)
    doc.append(SEC2)
    verify(doc.render())


SEC1_WITH_PREAMBLE = """
The first preamble

# First H1

First H1 section
"""

SEC2_WITH_PREAMBLE = """
The second preamble

# Second H1

Second H1 section
"""


def test_two_sections_of_the_same_level_with_preambles_can_be_prepended():
    doc = Doc.from_md(SEC2_WITH_PREAMBLE)
    doc.prepend(SEC1_WITH_PREAMBLE)
    assert len(doc.sections) == 2
    assert len(doc.preamble) != 0
    assert doc.metadata == {}
    assert doc.sections[0].title == "First H1"
    assert doc.sections[0].level == 1
    assert doc.sections[1].title == "Second H1"
    assert doc.sections[1].level == 1
    verify(pformat(doc, width=120, sort_dicts=False))


# noinspection PyPep8
def test_two_prepended_sections_of_the_same_level_with_preambles_can_be_rendered():
    doc = Doc.from_md(SEC2_WITH_PREAMBLE)
    doc.prepend(SEC1_WITH_PREAMBLE)
    verify(doc.render())


def test_two_sections_of_the_same_level_with_preambles_can_be_appended():
    doc = Doc.from_md(SEC1_WITH_PREAMBLE)
    doc.append(SEC2_WITH_PREAMBLE)
    assert len(doc.sections) == 2
    assert len(doc.preamble) != 0
    assert doc.metadata == {}
    assert doc.sections[0].title == "First H1"
    assert doc.sections[0].level == 1
    assert doc.sections[1].title == "Second H1"
    assert doc.sections[1].level == 1
    verify(pformat(doc, width=120, sort_dicts=False))


# noinspection PyPep8
def test_two_appended_sections_of_the_same_level_with_preambles_can_be_rendered():
    doc = Doc.from_md(SEC1_WITH_PREAMBLE)
    doc.append(SEC2_WITH_PREAMBLE)
    verify(doc.render())


AN_H1 = """
# An H1 Heading

Some H1 Heading text
"""

AN_H2 = """
## An H2 Heading

Some H2 Heading text
"""


# noinspection PyPep8
def test_prepending_a_lower_level_heading_to_a_higher_level_heading_will_cause_the_higher_level_heading_to_nest():
    doc = Doc.from_md(AN_H2)
    doc.prepend(AN_H1)
    assert len(doc.sections) == 1
    assert doc.sections[0].title == "An H1 Heading"
    assert len(doc.sections[0].subsections) == 1
    assert doc.sections[0].subsections[0].title == "An H2 Heading"
    verify(pformat(doc, width=120, sort_dicts=False))


def test_prepending_a_higher_level_heading_to_a_lower_level_heading_will_NOT_cause_the_higher_level_heading_to_nest():
    doc = Doc.from_md(AN_H1)
    doc.prepend(AN_H2)
    assert len(doc.sections) == 2
    assert doc.sections[0].title == "An H2 Heading"
    assert doc.sections[1].title == "An H1 Heading"
    verify(pformat(doc, width=120, sort_dicts=False))


def test_prepended_nested_sections_can_be_rendered():
    doc = Doc.from_md(AN_H2)
    doc.prepend(AN_H1)
    verify(doc.render())


def test_prepended_sections_with_different_levels_can_be_rendered():
    doc = Doc.from_md(AN_H1)
    doc.prepend(AN_H2)
    verify(doc.render())


def test_appending_a_higher_level_heading_to_a_lower_level_heading_will_cause_the_higher_level_heading_to_nest():
    doc = Doc.from_md(AN_H1)
    doc.append(AN_H2)
    assert len(doc.sections) == 1
    assert doc.sections[0].title == "An H1 Heading"
    assert len(doc.sections[0].subsections) == 1
    assert doc.sections[0].subsections[0].title == "An H2 Heading"
    verify(pformat(doc, width=120, sort_dicts=False))


def test_appending_a_lower_level_heading_to_a_higher_level_heading_will_NOT_cause_the_lower_level_heading_to_nest():
    doc = Doc.from_md(AN_H2)
    doc.append(AN_H1)
    assert len(doc.sections) == 2
    assert doc.sections[0].title == "An H2 Heading"
    assert doc.sections[1].title == "An H1 Heading"
    verify(pformat(doc, width=120, sort_dicts=False))


def test_appended_nested_sections_can_be_rendered():
    doc = Doc.from_md(AN_H1)
    doc.append(AN_H2)
    verify(doc.render())


def test_appended_sections_with_different_levels_can_be_rendered():
    doc = Doc.from_md(AN_H2)
    doc.append(AN_H1)
    verify(doc.render())


NESTED_SECTIONS1 = """
# An H1

h1 text

## An H2

h2 text

## Another H2

more h2 text

### An H3

h3 text
"""

NESTED_SECTIONS2 = """
#### An h4

h4 text

### Another h3

more h3 text

## yet another h2

yet more h2 text

# Another h1?

For testing purposes
"""


def test_prepending_deeply_nested_documents_nest_sections_correctly():
    doc = Doc.from_md(NESTED_SECTIONS2)
    doc.prepend(NESTED_SECTIONS1)
    verify(pformat(doc, width=120, sort_dicts=False))


def test_prepended_deeply_nested_documents_render_correctly():
    doc = Doc.from_md(NESTED_SECTIONS2)
    doc.prepend(NESTED_SECTIONS1)
    verify(doc.render())


def test_appending_deeply_nested_documents_nest_sections_correctly():
    doc = Doc.from_md(NESTED_SECTIONS1)
    doc.append(NESTED_SECTIONS2)
    verify(pformat(doc, width=120, sort_dicts=False))


def test_appended_deeply_nested_documents_render_correctly():
    doc = Doc.from_md(NESTED_SECTIONS1)
    doc.append(NESTED_SECTIONS2)
    verify(doc.render())


def test_preambles_will_nest_into_the_rightmost_leaf_section_when_prepended_to():
    doc = Doc.from_md("The original preamble")
    doc.prepend(NESTED_SECTIONS1)
    assert len(doc.preamble) == 0
    verify(pformat(doc, width=120, sort_dicts=False))


def test_preambles_will_nest_into_the_rightmost_leaf_section_when_appended():
    doc = Doc.from_md(NESTED_SECTIONS1)
    doc.append("A new preamble")
    assert len(doc.preamble) == 0
    verify(pformat(doc, width=120, sort_dicts=False))
