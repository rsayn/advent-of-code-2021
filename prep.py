"""
Yes, I'm that lazy.
"""
import datetime
import pathlib
import urllib.request

from markdownify import markdownify as md


def prep_today() -> None:
    """
    Create folder for today's puzzle
    """
    day = get_formatted_day()
    folder = pathlib.Path(f'day{day}')
    if folder.exists():
        print(f'Skipping creation of {folder} since it already exists')
    inputfile = folder / 'input.txt'
    readme = folder / 'README.md'
    folder.mkdir()
    inputfile.touch()
    with open(readme, 'w') as readmefile:
        readmefile.write(get_readme_text())
    print('Done.')


def get_readme_text() -> str:
    """
    Reads the puzzle from AOC site.
    """
    now = datetime.datetime.now()
    url = f"https://adventofcode.com/{now.year}/day/{now.day}"
    html_text = read_url(url)
    start = html_text.index(f'<h2>--- Day {now.day}')
    end = html_text.index('</article>\\n')
    return md(html_text[start:end].replace('\\n', '\n'))

def read_url(url: str) -> str:
    """Reads an URL."""
    with urllib.request.urlopen(url) as page:
        return str(page.read())


def get_formatted_day() -> str:
    """Returns the current advent day, properly formatted."""
    now = datetime.datetime.now()
    if now.year != 2021 or now.month != 12:
        raise FromTheFutureException("Where we're going we don't need roads")
    return f"{now.day:02d}"


class FromTheFutureException(Exception):
    ...


if __name__ == '__main__':
    prep_today()
