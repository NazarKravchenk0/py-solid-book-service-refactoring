from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:  # only for type hints, no runtime import
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
            },
        )


class XmlSerializeStrategy(SerializeStrategy):
    def serialize(self, book: "Book") -> str:
        root = ET.Element("book")
        title_el = ET.SubElement(root, "title")
        title_el.text = book.title
        content_el = ET.SubElement(root, "content")
        content_el.text = book.content
        return ET.tostring(root, encoding="unicode")


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
            # Keep the same error message format
            raise ValueError(f"Unknown serialize type: {serialize_type}")
        return strategy.serialize(book)
