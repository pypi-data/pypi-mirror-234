from collections.abc import Iterable, Iterator, MutableMapping, Sequence
from pprint import PrettyPrinter
from typing import Self

import mdformat_footnote
import mdformat_frontmatter
import mdformat_tables
import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdformat.renderer import MDRenderer
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

from markie.rules import render_rules, wikilink_plugin
from markie.utils import generic_repr

__all__ = ["Doc", "Section"]

MD = (
    MarkdownIt('commonmark', {'breaks': True, 'html': True})
    .use(wikilink_plugin)
    .use(front_matter_plugin)
    .use(footnote_plugin)
    .enable('table')
)

RENDERER = MDRenderer()
OPTIONS = {
    "parser_extension": [
        render_rules,
        mdformat_tables,
        mdformat_footnote,
        mdformat_frontmatter,
    ],
}

StrMap = MutableMapping[str, "str | bool | int | float | StrMap"]

HEADING_LEVELS = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}


class Section:
    """
    A markdown section – This is mostly an ordered tree wrapper around a
    list of Tokens.
    """

    def __init__(
          self,
          heading: list[Token],
          preamble: list[Token] = None,
          subsections: list["Section"] = None,
    ):
        """
        :param heading: three markdown-it Tokens for a parsed heading tag
        :param preamble: a list of tokens between the heading title and the
            first subsection
        :param subsections: a list of this section's Sub-subsections
        """
        self.heading = heading
        self.preamble = preamble if preamble is not None else []
        self.subsections = subsections if subsections is not None else []

    @classmethod
    def from_md(cls, src: str) -> Self:
        """
        Parses the given markdown src string and returns a new Section.

        :param src: A string of markdown
        :raises ValueError: If the given markdown has multiple headings with
            the lowest heading level (e.g. two h2 headings) or if the given
            markdown contains a preamble
        """
        tokens = MD.parse(src)
        return cls.from_tokens(tokens)

    @classmethod
    def from_tokens(cls, src: Sequence[Token]) -> Self:
        """
        Creates a new Section from a sequence of markdown-it tokens

        :param src: A sequence of markdown-it tokens
        :raises ValueError: If the given markdown has multiple headings with
            the lowest heading level (e.g. two h2 headings) or if the given
            markdown contains a preamble
        """
        _, preamble, sections = parse(src)
        if len(sections) != 1 or preamble:
            raise ValueError(
                "The given markdown does not consist of a single section"
            )
        return sections[0]

    @property
    def level(self) -> int:
        """The level of this section (i.e. 1-6 corresponding to h1-h6)"""
        return HEADING_LEVELS[self.heading[0].tag]

    @property
    def title(self) -> str:
        """The raw unformatted title text of this section"""
        return self.heading[1].content

    @title.setter
    def title(self, value: str) -> None:
        """
        Sets the title of this section – the value string should be inline
        markdown.
        Be Warned — This function does not prevent the title from being
        set to non-inline text — behaviour is undefined if it is.
        """
        _, content, _ = MD.parse(value)
        self.heading[1] = content

    def prepend(self, src: "str | Section") -> None:
        """
        Prepends the given markdown string or Section *inside* this Section,
        attempting to maintain a tree-like Section structure.
        Metadata in the given src string is ignored.

        Note: this function does not prevent nonsensical operations such as
        prepending an H1 section inside an H2 section — the behaviour of this
        class is undefined in such cases.

        :param src: A string of Markdown text or a Section object
        """
        if isinstance(src, str):
            _, preamble, sections = parse(MD.parse(src))
        else:
            preamble, sections = [], [src]

        if not sections:
            self.preamble = [*preamble, *self.preamble]
        else:
            sections[-1].last().preamble.extend(self.preamble)
            self.preamble = preamble
            while (
                  self.subsections
                  and self.subsections[0].level > sections[-1].level
            ):
                current = sections[-1]
                while (
                      current.subsections
                      and self.subsections[0].level - 1 > current.level
                ):
                    current = current.subsections[-1]
                current.subsections.append(self.subsections.pop(0))
            self.subsections = [*sections, *self.subsections]

    def append(self, src: "str | Section") -> None:
        """
        Appends the given markdown string or Section to this Section,
        attempting to maintain a tree-like Section structure.
        Metadata in the given src string is ignored.

        Note: this function does not prevent nonsensical operations such as
        appending an H1 section inside an H2 section — the behaviour of this
        class is undefined in such cases.

        :param src: A string of Markdown text or a Section object
        """
        if isinstance(src, str):
            _, preamble, sections = parse(MD.parse(src))
        else:
            preamble, sections = [], [src]

        if not self.subsections:
            self.preamble.extend(preamble)
            self.subsections = sections
        else:
            self.subsections[-1].last().preamble.extend(preamble)
            while sections and self.subsections[-1].level < sections[0].level:
                current = self.subsections[-1]
                while sections[0].level - 1 > current.level:
                    current = current.subsections[-1]
                current.subsections.append(sections.pop(0))
            self.subsections = [*self.subsections, *sections]

    def last(self) -> "Section":
        """Returns the last ("rightmost") node in the section tree"""
        if self.subsections:
            return self.subsections[-1].last()
        else:
            return self

    def render(self) -> str:
        """Renders this section as markdown"""
        return RENDERER.render([*self], OPTIONS, {})

    def __iter__(self) -> Iterator[Token]:
        """
        Iterates over the tokens in this section and its subsections in order
        """
        yield from self.heading
        yield from self.preamble
        for subsection in self.subsections:
            yield from subsection

    def __repr__(self):
        return generic_repr(self)


class Doc:
    """
    A Markdown document with metadata.

    Parses Markdown text into metadata, a preamble, and Sections. Doc objects
    attempt to parse sections into a tree like-structure; however,
    this assumes markdown is "well formatted" with sections following a
    natural order (i.e. h1 -> h2 -> h3). This class does not prevent users
    from breaking this order, but its behaviour in such cases is undefined.

    Elements in the Doc preamble, and Sections consist of markdown-it Tokens
    and can be manipulated directly.
    """

    def __init__(
          self,
          metadata: StrMap,
          preamble: list[Token],
          sections: list[Section]
    ):
        """
        :param metadata: a mapping of markdown metadata
        :param preamble: a list of markdown-it Tokens that appear between the
            metadata and first heading
        :param sections: the document sections as an AST
        """
        self.metadata = metadata
        self.preamble = preamble
        self.sections = sections

    @classmethod
    def from_md(cls, src: str) -> Self:
        """
        Parses the given markdown src string and returns a new Doc.

        :param src: A string of markdown
        """
        tokens = MD.parse(src)
        return cls.from_tokens(tokens)

    @classmethod
    def from_tokens(cls, src: Sequence[Token]) -> Self:
        """
        Creates a new Doc from a sequence of markdown-it tokens

        :param src: A sequence of markdown-it tokens
        """
        frontmatter, preamble, sections = parse(src)
        return cls(frontmatter, preamble, sections)

    def prepend(self, src: str) -> None:
        """
        Prepends the given src markdown to this document, attempting to
        maintain a tree-like Section structure. Any metadata in the given src
        string is ignored

        :param src: The Markdown src string
        """
        _, preamble, sections = parse(MD.parse(src))
        if not sections:
            self.preamble = [*preamble, *self.preamble]
        else:
            sections[-1].last().preamble.extend(self.preamble)
            self.preamble = preamble
            while self.sections and self.sections[0].level > sections[-1].level:
                sections[-1].append(self.sections.pop(0))
            self.sections = [*sections, *self.sections]

    def append(self, src: str) -> None:
        """
        Appends the given Markdown src string to this document, attempting to
        maintain a tree-like Section structure. Any metadata in the given src
        string is ignored

        :param src: The Markdown src string
        """
        _, preamble, sections = parse(MD.parse(src))
        if not self.sections:
            self.preamble.extend(preamble)
            self.sections = sections
        else:
            self.sections[-1].last().preamble.extend(preamble)
            while sections and self.sections[-1].level < sections[0].level:
                self.sections[-1].append(sections.pop(0))
            self.sections = [*self.sections, *sections]

    def render(self) -> str:
        """Renders this doc as markdown"""
        if self.metadata:
            frontmatter = as_frontmatter(self.metadata)
            return RENDERER.render([frontmatter, *self], OPTIONS, {})
        else:
            return RENDERER.render(list(self), OPTIONS, {})

    def __iter__(self) -> Iterator[Token]:
        """Iterates over the Tokens of this document in order"""
        yield from self.preamble
        for section in self.sections:
            yield from section

    def __repr__(self):
        return generic_repr(self)


def parse(src: Iterable[Token]) -> tuple[StrMap, list[Token], list[Section]]:
    """
    Parses a markdown-it Token stream to metadata, a preamble, and
    nested Sections

    :param src: An Iterable of markdown-it Tokens
    :return: a tuple of the metadata, preamble, and Section tree in that order.
    """
    metadata = {}
    preamble = []
    stack = []
    tokens = iter(src)
    for token in tokens:
        if token.type == "front_matter":
            metadata = yaml.safe_load(token.content)
        elif token.type == "heading_open":
            level = HEADING_LEVELS[token.tag]
            while (len(stack) > 1
                   and level <= stack[-1].level
                   and stack[-2].level < stack[-1].level):
                stack[-2].subsections.append(stack.pop())
            heading = [token, next(tokens), next(tokens)]
            stack.append(Section(heading))
        elif stack:
            stack[-1].preamble.append(token)
        else:
            preamble.append(token)
    while len(stack) > 1 and stack[-2].level < stack[-1].level:
        stack[-2].subsections.append(stack.pop())
    return metadata, preamble, stack


def as_frontmatter(metadata: StrMap) -> Token:
    """Maps frontmatter data to a markdown-it Token"""
    return Token(
        type='front_matter',
        tag='',
        nesting=0,
        content=yaml.safe_dump(metadata, sort_keys=False),
        markup='---',
        block=True,
        hidden=True,
    )


def render(tokens: Sequence[Token]):
    """Shortcut to render with default options"""
    return RENDERER.render(tokens, OPTIONS, {})


# noinspection PyUnresolvedReferences,PyProtectedMember,PyMethodMayBeStatic
class _DocPrettyPrinter(PrettyPrinter):
    """
    Pretty printer for Doc and Section objects.

    Note: The output of this pretty printer is used in approval tests to
    check Markdown document structure.
    """

    def _pprint_doc(self, obj, stream, indent, *args):
        stream.write(f"Doc(")
        indent += 4
        stream.write(f"metadata=")
        self._format(obj.metadata, stream, indent + 9, *args)
        stream.write(f",\n{' ' * indent}preamble=")
        preamble = render(obj.preamble).strip()
        self._format(preamble, stream, indent + 9, *args)
        stream.write(f",\n{' ' * indent}sections=")
        self._format(obj.sections, stream, indent + 9, *args)
        stream.write(f")")

    def _pprint_section(self, obj, stream, indent, *args):
        stream.write(f"Section(")
        indent += 8
        stream.write(f"level=")
        self._format(obj.level, stream, indent + 6, *args)
        stream.write(f",\n{' ' * indent}title=")
        heading = obj.title.strip()
        self._format(heading, stream, indent + 6, *args)
        stream.write(f",\n{' ' * indent}preamble=")
        preamble = render(obj.preamble).strip()
        self._format(preamble, stream, indent + 9, *args)
        stream.write(f",\n{' ' * indent}subsections=")
        self._format(obj.subsections, stream, indent + 12, *args)
        stream.write(f")")

    PrettyPrinter._dispatch[Doc.__repr__] = _pprint_doc
    PrettyPrinter._dispatch[Section.__repr__] = _pprint_section
