"""Builder pattern demo: build HTML step-by-step with a director + builder."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import html

@dataclass
class Node:
    tag: str
    attrs: Dict[str, str] = field(default_factory=dict)
    children: List["Node"] = field(default_factory=list)  # fixed type ref
    text: Optional[str] = None
    void: bool = False  # added: was used but not defined

    def render(self, indent=0, step=2) -> str:
        pad = " " * indent
        attrs = "".join(f' {k}="{html.escape(v, quote=True)}"' for k, v in self.attrs.items())
        if self.void:
            return f"{pad}<{self.tag}{attrs} />\n"
        if self.children:
            inner = "".join(c.render(indent + step, step) for c in self.children)
            return f"{pad}<{self.tag}{attrs}>\n{inner}{pad}</{self.tag}>\n"
        if self.text is not None:
            return f"{pad}<{self.tag}{attrs}>{html.escape(self.text, quote=True)}</{self.tag}>\n"
        return f"{pad}<{self.tag}{attrs}></{self.tag}>\n"


# ---- Builder ----------------------------------------------------
class HtmlBuilder:
    VOID = {"meta", "link", "img", "br", "hr", "input"}

    def __init__(self, root_tag="html", **attrs):
        self.root = Node(root_tag, dict(attrs))
        self._stack = [self.root]

    # fluent steps
    def start(self, tag: str, **attrs) -> "HtmlBuilder":
        node = Node(tag=tag, attrs=dict(attrs), void=(tag in self.VOID))  # fixed: void kw
        self._stack[-1].children.append(node)
        if not node.void:
            self._stack.append(node)
        return self

    def text(self, s: str) -> "HtmlBuilder":
        self._stack[-1].text = s
        return self

    def attr(self, key: str, val: str) -> "HtmlBuilder":
        self._stack[-1].attrs[key] = val
        return self

    def end(self) -> "HtmlBuilder":
        if len(self._stack) <= 1:
            raise RuntimeError("Nothing to end: at root.")
        self._stack.pop()
        return self

    def build(self) -> str:
        if len(self._stack) != 1:
            raise RuntimeError("Unbalanced: not all elements were closed.")
        return "<!DOCTYPE html>\n" + self.root.render()


def simple_page(title: str, body_text: str) -> str:
    b = HtmlBuilder("html", lang="en")
    (
        b.start("head")
            .start("meta", charset="utf-8")
            .start("title").text(title).end()
        .end()
        .start("body")
            .start("h1").text(title).end()
            .start("p").text(body_text).end()  # now uses body_text
        .end()
    )
    return b.build()


print(simple_page("Builder Pattern (Mini)", "This page was built with a tiny builder."))
