from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:  # only for type hints, no runtime import
    from app.main import Book


class PrintStrategy(ABC):
    @abstractmethod
    def print_book(self, book: "Book") -> None:
        ...


class ConsolePrintStrategy(PrintStrategy):
    def print_book(self, book: "Book") -> None:
        print(f"Printing the book: {book.title}...")
        print(book.content)


class ReversePrintStrategy(PrintStrategy):
    def print_book(self, book: "Book") -> None:
        print(f"Printing the book in reverse: {book.title}...")
        print(book.content[::-1])


class BookPrinter:
    """Service responsible only for printing the book."""

    def __init__(self) -> None:
        self._strategies: Dict[str, PrintStrategy] = {
            "console": ConsolePrintStrategy(),
            "reverse": ReversePrintStrategy(),
        }

    def print(self, book: "Book", print_type: str) -> None:
        strategy = self._strategies.get(print_type)
        if strategy is None:
            # Keep the same error message format
            raise ValueError(f"Unknown print type: {print_type}")
        strategy.print_book(book)
