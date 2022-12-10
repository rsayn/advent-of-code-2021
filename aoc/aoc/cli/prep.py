"""
Yes, I'm that lazy.
"""
import re
import datetime
from pathlib import Path
from typing import Tuple
import urllib.request

from markdownify import markdownify as md


def prep_today():
    """
    Create folder for today's puzzle
    """
    year, day = get_year_and_day()
    folder = create_puzzle_folder(year, day)
    aoc_puzzle = get_aoc_puzzle(year, day)

    create_readme(folder, aoc_puzzle)
    create_python_file(folder, aoc_puzzle)
    create_input_files(folder)

    print('Done.')


def get_year_and_day() -> Tuple[str, str]:
    """
    Returns the current advent day, properly formatted.
    """
    now = datetime.datetime.now()
    if now.month != 12:
        raise ValueError("This is not that time of the year! Try again in december 🎄")
    return str(now.year), f"{now.day:02d}"


def create_puzzle_folder(year: str, day: str):
    puzzle_folder = Path(f"aoc_{year}", f"day{day}")
    if puzzle_folder.exists():
        raise ValueError("Skipping creation: folder already exists")
    puzzle_folder.mkdir(parents=True)
    return puzzle_folder


def get_aoc_puzzle(year: str, day: str) -> str:
    """
    Reads the puzzle from AOC site.
    """
    day_number = day.lstrip('0')
    url = f"https://adventofcode.com/{year}/day/{day_number}"
    html_text = read_url(url)
    start = html_text.index(f'<h2>--- Day {day_number}')
    end = html_text.index('</article>\\n')
    return md(html_text[start:end].replace('\\n', '\n'))


def read_url(url: str) -> str:
    """
    Reads an URL.
    """
    with urllib.request.urlopen(url) as page:
        return str(page.read())


def create_readme(folder: Path, aoc_puzzle: str):
    readme_path = Path(folder, "README.md")
    readme_path.touch()
    readme_path.write_text(aoc_puzzle)


def create_python_file(folder: Path, aoc_puzzle: str):
    filename = get_puzzle_title(aoc_puzzle).lower().replace(" ", "_")
    python_file = Path(folder, f"{filename}.py")
    python_file.touch()
    template_file = Path(__file__).parent.parent / "templates" / "day_template.py"
    python_file.write_text(template_file.read_text())


def create_input_files(folder: Path):
    Path(folder, "input.txt").touch()
    Path(folder, "sample_input.txt").touch()


def get_puzzle_title(puzzle_text: str) -> str:
    """
    Returns the puzzle title.
    """
    return re.match(r'--- Day [0-9]+: ([A-Za-z\s-]+) ---', puzzle_text)[1]
