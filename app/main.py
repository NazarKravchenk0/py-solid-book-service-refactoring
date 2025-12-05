from __future__ import annotations

from app.display import BookDisplayer
from app.printer import BookPrinter
from app.serializer import BookSerializer


class Book:
    """Entity that stores book data only.

    All operations (display / print / serialize) are delegated
    to separate service classes to follow SRP and DIP.
    """

    def __init__(
        self,
        title: str,
        content: str,
        displayer: BookDisplayer | None = None,
        printer: BookPrinter | None = None,
        serializer: BookSerializer | None = None,
    ):
        self.title = title
        self.content = content
        # Dependencies are injected (with sensible defaults).
        # This keeps backward compatibility and still respects DIP.
        self._displayer = displayer or BookDisplayer()
        self._printer = printer or BookPrinter()
        self._serializer = serializer or BookSerializer()

    def display(self, display_type: str) -> None:
        """Facade method kept for backward compatibility."""
        self._displayer.display(self, display_type)

    def print_book(self, print_type: str) -> None:
        """Facade method kept for backward compatibility."""
        self._printer.print(self, print_type)

    def serialize(self, serialize_type: str) -> str:
        """Facade method kept for backward compatibility."""
        return self._serializer.serialize(self, serialize_type)


def main(book: Book, commands: list[tuple[str, str]]) -> str | None:
    """Orchestrates operations on a book based on commands list.

    commands: list of tuples (command_name, command_type)
        command_name in {"display", "print", "serialize"}
        command_type depends on command:
            - display: "console" / "reverse"
            - print: "console" / "reverse"
            - serialize: "json" / "xml"
    """
    for cmd, method_type in commands:
        if cmd == "display":
            book.display(method_type)
        elif cmd == "print":
            book.print_book(method_type)
        elif cmd == "serialize":
            # return first serialization result
            return book.serialize(method_type)
    return None


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    result = main(
        sample_book,
        [("display", "reverse"), ("serialize", "xml")],
    )
    if result is not None:
        print(result)
