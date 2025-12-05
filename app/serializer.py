from __future__ import annotations

import json
import xml.etree.ElementTree as element_tree
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from app.main import Book


class SerializeStrategy(ABC):
    @abstractmethod
    def serialize(self, book: "Book") -> str:
        ...


class JsonSerializeStrategy(SerializeStrategy):
    def serialize(self, book: "Book") -> str:
        return json.dumps(
            {
                "title": book.title,
                "content": book.content,
            }
        )


class XmlSerializeStrategy(SerializeStrategy):
    def serialize(self, book: "Book") -> str:
        root = element_tree.Element("book")
        title_el = element_tree.SubElement(root, "title")
        title_el.text = book.title
        content_el = element_tree.SubElement(root, "content")
        content_el.text = book.content
        return element_tree.tostring(root, encoding="unicode")


class BookSerializer:
    """Service responsible only for serialization of the book."""

    def __init__(self) -> None:
        self._strategies: Dict[str, SerializeStrategy] = {
            "json": JsonSerializeStrategy(),
            "xml": XmlSerializeStrategy(),
        }

    def serialize(self, book: "Book", serialize_type: str) -> str:
        strategy = self._strategies.get(serialize_type)
        if strategy is None:
            raise ValueError(f"Unknown serialize type: {serialize_type}")
        return strategy.serialize(book)
