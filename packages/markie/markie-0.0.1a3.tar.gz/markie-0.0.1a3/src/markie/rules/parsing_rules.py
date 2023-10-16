from markdown_it.rules_inline import StateInline


def wikilink_plugin(md):
    md.inline.ruler.before(
        "link",
        "wikilink",
        wikilink_rule,
    )


def wikilink_rule(state: StateInline, silent: bool) -> bool:
    start = state.pos
    pos = state.pos
    src = state.src

    if src[pos:pos+2] == "[[":
        pos += 2
    elif src[pos:pos + 3] == "![[":
        pos += 3
    else:
        return False

    while pos < state.posMax and src[pos] not in ("\n", "]"):
        pos += 1

    if src[pos:pos + 2] == "]]":
        pos += 2
    else:
        return False

    end = pos

    if not silent:
        token = state.push("wikilink", "", 0)
        token.content = src[start:end]
        # note, this is not part of markdown-it JS, but is useful for renderers
        if state.md.options.get("store_labels", False):
            token.meta["label"] = token.content

    state.pos = end
    return True
