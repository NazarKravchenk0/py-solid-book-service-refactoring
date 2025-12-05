import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class Book:
    """Entity that stores book data only.

    All operations (display / print / serialize) are delegated
    to separate service classes to follow SRP.
    """

    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        # Delegation to separate services (composition)
        self._displayer = BookDisplayer()
        self._printer = BookPrinter()
        self._serializer = BookSerializer()

    def display(self, display_type: str) -> None:
        """Facade method kept for backward compatibility."""
        self._displayer.display(self, display_type)

    def print_book(self, print_type: str) -> None:
        """Facade method kept for backward compatibility."""
        self._printer.print(self, print_type)

    def serialize(self, serialize_type: str) -> str:
        """Facade method kept for backward compatibility."""
        return self._serializer.serialize(self, serialize_type)


# ===== Display responsibility =====


class DisplayStrategy(ABC):
    @abstractmethod
    def display(self, book: Book) -> None:
        ...


class ConsoleDisplayStrategy(DisplayStrategy):
    def display(self, book: Book) -> None:
        print(book.content)


class ReverseDisplayStrategy(DisplayStrategy):
    def display(self, book: Book) -> None:
        print(book.content[::-1])


class BookDisplayer:
    """Service responsible only for how the book is displayed."""

    _strategies: dict[str, DisplayStrategy]

    def __init__(self) -> None:
        self._strategies = {
            "console": ConsoleDisplayStrategy(),
            "reverse": ReverseDisplayStrategy(),
        }

    def display(self, book: Book, display_type: str) -> None:
        strategy = self._strategies.get(display_type)
        if strategy is None:
            # Keep exactly the same error message as in original code
            raise ValueError(f"Unknown display type: {display_type}")
        strategy.display(book)


# ===== Print responsibility =====


class PrintStrategy(ABC):
    @abstractmethod
    def print_book(self, book: Book) -> None:
        ...


class ConsolePrintStrategy(PrintStrategy):
    def print_book(self, book: Book) -> None:
        print(f"Printing the book: {book.title}...")
        print(book.content)


class ReversePrintStrategy(PrintStrategy):
    def print_book(self, book: Book) -> None:
        print(f"Printing the book in reverse: {book.title}...")
        print(book.content[::-1])


class BookPrinter:
    """Service responsible only for printing the book."""

    _strategies: dict[str, PrintStrategy]

    def __init__(self) -> None:
        self._strategies = {
            "console": ConsolePrintStrategy(),
            "reverse": ReversePrintStrategy(),
        }

    def print(self, book: Book, print_type: str) -> None:
        strategy = self._strategies.get(print_type)
        if strategy is None:
            # Keep the same error message format
            raise ValueError(f"Unknown print type: {print_type}")
        strategy.print_book(book)


# ===== Serialization responsibility =====


class SerializeStrategy(ABC):
    @abstractmethod
    def serialize(self, book: Book) -> str:
        ...


class JsonSerializeStrategy(SerializeStrategy):
    def serialize(self, book: Book) -> str:
        return json.dumps({"title": book.title, "content": book.content})


class XmlSerializeStrategy(SerializeStrategy):
    def serialize(self, book: Book) -> str:
        root = ET.Element("book")
        title_el = ET.SubElement(root, "title")
        title_el.text = book.title
        content_el = ET.SubElement(root, "content")
        content_el.text = book.content
        return ET.tostring(root, encoding="unicode")


class BookSerializer:
    """Service responsible only for serialization of the book."""

    _strategies: dict[str, SerializeStrategy]

    def __init__(self) -> None:
        self._strategies = {
            "json": JsonSerializeStrategy(),
            "xml": XmlSerializeStrategy(),
        }

    def serialize(self, book: Book, serialize_type: str) -> str:
        strategy = self._strategies.get(serialize_type)
        if strategy is None:
            # Keep the same error message format
            raise ValueError(f"Unknown serialize type: {serialize_type}")
        return strategy.serialize(book)


# ===== Orchestration (unchanged public behaviour) =====


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    for cmd, method_type in commands:
        if cmd == "display":
            book.display(method_type)
        elif cmd == "print":
            book.print_book(method_type)
        elif cmd == "serialize":
            return book.serialize(method_type)


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
