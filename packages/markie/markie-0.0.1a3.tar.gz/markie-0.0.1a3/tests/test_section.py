from pprint import pformat

import pytest
from approvaltests import verify

from markie import Section

SEC = """
# Strategies for Creative Problem Solving

The purpose of this book is to help problem solvers improve their street smarts.
"""


def test_a_single_section_can_be_parsed():
    section = Section.from_md(SEC)
    assert section.title == "Strategies for Creative Problem Solving"
    assert section.level == 1
    verify(pformat(section, width=120, sort_dicts=False))


def test_a_single_section_can_be_rendered():
    section = Section.from_md(SEC)
    verify(section.render())


def test_section_titles_can_be_changed():
    section = Section.from_md(SEC)
    assert section.title == "Strategies for Creative Problem Solving"
    section.title = "A Completely New Title!"
    assert section.title == "A Completely New Title!"
    verify(pformat(section, width=120, sort_dicts=False))


def test_section_titles_can_be_rendered_after_being_changed():
    section = Section.from_md(SEC)
    section.title = "A Completely New Title!"
    verify(section.render())


MULTIPLE_SECTIONS = """
## Heading Number 1

Content for heading number 1

## Heading Number 2

Content for heading number 2
"""


def test_multiple_sections_of_the_same_level_raise_a_value_error_when_parsed():
    with pytest.raises(ValueError):
        Section.from_md(MULTIPLE_SECTIONS)


SECTION_WITH_PREAMBLE = """
A preamble

## Heading Number 1

Content for heading number 1
"""


def test_markdown_containing_a_preamble_will_raise_a_value_error_when_parsed():
    with pytest.raises(ValueError):
        Section.from_md(SECTION_WITH_PREAMBLE)


SEC_WITH_METADATA = """
---
title: All About Envelopes
src: https://en.wikipedia.org/wiki/Windowed_envelope
---

## Envelopes

Satisfactorily-strong envelopes for business and general-purpose domestic
correspondence can be, and are, in fact, made out of paper of various qualities.
""".strip()


def test_metadata_is_ignored_when_parsing_sections():
    section = Section.from_md(SEC_WITH_METADATA)
    assert section.title == "Envelopes"
    assert section.level == 2
    verify(pformat(section, width=120, sort_dicts=False))


NESTED_SECTIONS = """
## Heading 1

Content for heading number 1

### Heading 1-1

Content for heading number 1-1

### Heading 1-2

Content for heading number 1-2
"""


def test_nested_sections_can_be_parsed():
    section = Section.from_md(NESTED_SECTIONS)
    assert len(section.preamble) != 0
    assert len(section.subsections) == 2
    assert section.title == "Heading 1"
    assert section.subsections[0].title == "Heading 1-1"
    assert section.subsections[1].title == "Heading 1-2"
    verify(pformat(section, width=120, sort_dicts=False))


def test_nested_sections_can_be_rendered():
    section = Section.from_md(NESTED_SECTIONS)
    verify(section.render())


PARA = "A completely new paragraph of text!!"


def test_a_paragraph_of_text_can_be_prepended_to_a_section():
    section = Section.from_md(SEC)
    section.prepend(PARA)
    verify(pformat(section, width=120, sort_dicts=False))


def test_a_paragraph_of_text_prepended_to_a_section_renders_correctly():
    section = Section.from_md(SEC)
    section.prepend(PARA)
    verify(section.render())


def test_a_paragraph_of_text_can_be_appended_to_a_section():
    section = Section.from_md(SEC)
    section.append(PARA)
    verify(pformat(section, width=120, sort_dicts=False))


def test_a_paragraph_of_text_appended_to_a_section_renders_correctly():
    section = Section.from_md(SEC)
    section.append(PARA)
    verify(section.render())


SEC1 = """
# An H1 Section

H1 section body
"""

SEC2 = """
## An H2 Section

H2 section body
"""


def test_an_h2_section_can_be_prepended_to_an_h1_section():
    section = Section.from_md(SEC1)
    section.prepend(SEC2)
    assert len(section.subsections) == 1
    assert section.subsections[0].title == "An H2 Section"
    verify(pformat(section, width=120, sort_dicts=False))


def test_an_h2_section_prepended_to_an_h1_section_renders_correctly():
    section = Section.from_md(SEC1)
    section.prepend(SEC2)
    verify(section.render())


def test_an_h2_section_can_be_appended_to_an_h1_section():
    section = Section.from_md(SEC1)
    section.append(SEC2)
    assert len(section.subsections) == 1
    assert section.subsections[0].title == "An H2 Section"
    verify(pformat(section, width=120, sort_dicts=False))


def test_an_h2_section_appended_to_an_h1_section_renders_correctly():
    section = Section.from_md(SEC1)
    section.append(SEC2)
    verify(section.render())


def test_an_h2_section_object_can_be_prepended_to_an_h1_section_object():
    section1 = Section.from_md(SEC1)
    section2 = Section.from_md(SEC2)
    section1.prepend(section2)
    verify(pformat(section1, width=120, sort_dicts=False))


def test_an_h2_section_object_can_be_appended_to_an_h1_section_object():
    section1 = Section.from_md(SEC1)
    section2 = Section.from_md(SEC2)
    section1.append(section2)
    verify(pformat(section1, width=120, sort_dicts=False))


SEC2_WITH_PREAMBLE = """
Some preamble before Section 2

## An H2 Section

H2 section body
"""


def test_an_h2_section_with_a_preamble_can_be_prepended_to_an_h1_section():
    section = Section.from_md(SEC1)
    section.prepend(SEC2_WITH_PREAMBLE)
    assert len(section.subsections) == 1
    assert section.subsections[0].title == "An H2 Section"
    verify(pformat(section, width=120, sort_dicts=False))


def test_an_h2_section_with_a_preamble_prepended_to_an_h1_section_renders_correctly():
    section = Section.from_md(SEC1)
    section.prepend(SEC2_WITH_PREAMBLE)
    verify(section.render())


def test_an_h2_section_with_a_preamble_can_be_appended_to_an_h1_section():
    section = Section.from_md(SEC1)
    section.append(SEC2_WITH_PREAMBLE)
    assert len(section.subsections) == 1
    assert section.subsections[0].title == "An H2 Section"
    verify(pformat(section, width=120, sort_dicts=False))


def test_an_h2_section_with_a_preamble_appended_to_an_h1_section_renders_correctly():
    section = Section.from_md(SEC1)
    section.append(SEC2_WITH_PREAMBLE)
    verify(section.render())


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
## yet another h2

yet more h2 text

### Another h3

more h3 text

#### An h4

h4 text
"""

NESTED_SECTIONS3 = """
#### An h4

h4 text

### Another h3

more h3 text

## yet another h2

yet more h2 text
"""


def test_prepending_deeply_nested_sections_nest_sections_correctly():
    section = Section.from_md(NESTED_SECTIONS1)
    section.prepend(NESTED_SECTIONS2)
    verify(pformat(section, width=120, sort_dicts=False))


def test_prepended_deeply_nested_sections_render_correctly():
    section = Section.from_md(NESTED_SECTIONS1)
    section.prepend(NESTED_SECTIONS2)
    verify(section.render())


def test_appending_deeply_nested_documents_nest_sections_correctly():
    section = Section.from_md(NESTED_SECTIONS1)
    section.append(NESTED_SECTIONS3)
    verify(pformat(section, width=120, sort_dicts=False))


def test_appended_deeply_nested_documents_render_correctly():
    section = Section.from_md(NESTED_SECTIONS1)
    section.append(NESTED_SECTIONS3)
    verify(section.render())


NESTED_SECTIONS4 = """
# An H1

Some H1 Text

#### An h4

Some h4 text

## yet another h2

yet more h2 text
"""

SEC3 = """
## A new H2

Some new H2 text

### A new H3

Some new H3 text

## Another new H2

More new H2 text

### Another new H3

More new H3 text
"""


def test_prepending_a_heading_with_lower_rank_than_the_first_subheading_will_cause_the_subheading_to_nest():
    section = Section.from_md(NESTED_SECTIONS4)
    section.prepend(SEC3)
    verify(pformat(section, width=120, sort_dicts=False))
