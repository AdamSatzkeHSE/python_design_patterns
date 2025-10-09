""" When we want to create an object that is composed of multiple parts and 
the composition needs to be done step by step. The object is not complete unless all its
parts are fully created.

The builder pattern separates the construction of a complex object from its representation
By keeping the construction separate from the representation, the same construction can be used
to create several different represenatations.
"""

# The Builder: The component responsible for creating various parts of a complex object.
# HTML: title, head, body

# The director: The component that controls the building process using a builder instance.
# It calls the builders functions for setting the title, the heading and so on.

# Using different builder instances let's us create different HTML pages without touchgin any of the
# code of the director.

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import html

@dataclass
class Node:
    tag: str
    attrs: Dict[str, str] = field(default_factory=dict)
    children: List["node"] = field(default_factory=list)
    text: Optional[str] = None


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
        node = Node(tag, dict(attrs), void=(tag in self.VOID))
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
        .start("meta", charset="utf-8").end()
        .start("title").text(title).end()
        .end()

        .start("body")
        .start("h1").text(title).end()
        .end()
    )

    return b.build()

print(simple_page("Builder Pattern (Mini)", "This page was built with a tiny builder."))