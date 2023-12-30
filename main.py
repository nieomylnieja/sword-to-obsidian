#!/usr/bin/env python3

import argparse
import os
import json
from dataclasses import dataclass

from pysword.modules import SwordModules


@dataclass
class Book:
    """Single Bible book representation."""

    name: str
    chapters: list[list[str]]


@dataclass
class Locale:
    """Locale mappings for the whole Bible."""

    name: str
    books: dict[str, str]


def main():
    parser = argparse.ArgumentParser(
        prog="sword-to-obsidian",
        description="A Python program which converts SWORD Bible module to Obsidian Markdown.",
    )
    parser.add_argument("path", help="Path to the SWORD module")
    parser.add_argument(
        "-l",
        "--locale",
        help="Path to JSON locale to use",
        required=False,
        default="loc/pl.json",
    )
    args = parser.parse_args()

    locale = read_locale(args.locale)
    books = parse_module(args.path, locale)

    convert_to_obsidian(books, locale)


def parse_module(path: str, locale: Locale) -> list[Book]:
    modules = SwordModules(path)
    modules.parse_modules()
    module_name = os.path.splitext(os.path.basename(path))[0]
    bible = modules.get_bible_from_module(module_name)

    allBooks = [
        book for books in bible.get_structure().get_books().values() for book in books
    ]
    sep = "\n"
    result: list[Book] = []
    for book in allBooks:
        chapters: list[list[str]] = []
        for chapter in range(1, book.num_chapters):
            text = bible.get(books=book.name, chapters=chapter, clean=True, join=sep)
            verses = [verse.strip() for verse in text.split(sep)]
            chapters.append(verses)
        result.append(Book(locale.books[book.name], chapters))

    return result


def read_locale(loc_file: str) -> Locale:
    with open(loc_file, "r") as f:
        data = json.load(f)
        return Locale(**data)


def convert_to_obsidian(books: list[Book], locale: Locale) -> None:
    for book in books:
        write_book_file(locale, book)
        for i, chapter in enumerate(book.chapters):
            write_chapter_file(locale, book, i)


def write_book_file(locale: Locale, book: Book) -> None:
    dir = os.path.join(locale.name, book.name)
    os.makedirs(dir, exist_ok=True)
    file_path = os.path.join(dir, f"{book.name}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(
            f"""links: [[Bible]]
# {book.name}

[[{book.name} 1|Rozpocznij czytanie →]]"""
        )


def write_chapter_file(locale: Locale, book: Book, chapter_index: int) -> None:
    dir = os.path.join(locale.name, book.name)
    os.makedirs(dir, exist_ok=True)
    chapter = chapter_index + 1
    file_path = os.path.join(dir, f"{book.name} {chapter}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        refs = f"[[{book.name}]]"
        if chapter > 1:
            refs = f"[[{book.name} {chapter-1}|← {book.name} {chapter-1}]] | {refs}"
        if chapter < len(book.chapters):
            refs = f"{refs} | [[{book.name} {chapter+1}|{book.name} {chapter+1} →]]"
        verses = "\n".join(
            [
                f"###### {i+1}\n{verse}"
                for i, verse in enumerate(book.chapters[chapter_index])
            ]
        )
        f.write(
            f"""# {book.name} {chapter}

{refs}

***

{verses}

***

{refs}"""
        )


if __name__ == "__main__":
    main()
