from __future__ import annotations
from dataclasses import dataclass, field
from itertools import takewhile
import operator
from typing import *
from pathlib import Path


@dataclass
class Folder:
    name: str
    parent: Optional[Folder] = None
    contents: List[Union[File, Folder]] = field(default_factory=list)

    def __post_init__(self):
        for folder in self.folders:
            folder.parent = self

    def add_item(self, item: Union[File, Folder]):
        self.contents.append(item)
        if isinstance(item, Folder):
            item.parent = self

    def __contains__(self, item: str) -> bool:
        return any(element.name == item for element in self.contents)

    def __iter__(self) -> Iterator[Union[File, Folder]]:
        return iter(self.contents)

    def __getitem__(self, key: str):
        return next(item for item in self.contents if item.name == key)

    def iter_folders(self) -> Iterator[Folder]:
        for folder in self.folders:
            yield folder
            for subfolder in folder.iter_folders():
                yield subfolder

    @property
    def files(self) -> Iterator[File]:
        return (item for item in self.contents if isinstance(item, File))
    
    @property
    def folders(self) -> Iterator[Folder]:
        return (item for item in self.contents if isinstance(item, Folder))

    @property
    def size(self) -> int:
        return sum(item.size for item in self.contents)

    @property
    def root(self) -> Folder:
        folder = self
        while folder.parent is not None:
            folder = folder.parent
        return folder

    @property
    def fullpath(self) -> str:
        folder = self
        parts = []
        while folder.parent is not None:
            parts.append(folder.name)
            folder = folder.parent
        return "/" + ("/".join(reversed(parts)))

    def __repr__(self):
        tab = "  "
        folders = ["\n".join([f"{tab}{line}" for line in repr(folder).splitlines()]) for folder in self.folders]
        files = "\n".join([f"{tab}{file.name} ({file.size})" for file in self.files])
        return "\n".join([self.name, *folders, files])


@dataclass
class File:
    size: int
    name: str


def run_puzzle(filename: str):
    """
    Runs today's puzzle.
    """
    FOLDER = Path(__file__).parent
    puzzle_lines = list(read_puzzle_lines(FOLDER / filename))
    puzzle_content = parse_puzzle_lines(puzzle_lines)

    result_one = solve_part_one(puzzle_content)
    print(f"The result for part 1 is {result_one}")

    result_two = solve_part_two(puzzle_content)
    print(f"The result for part 2 is {result_two}")


def read_puzzle_lines(filepath: Path) -> Iterator[str]:
    """
    Reads the AOC puzzle input.
    """
    with open(filepath, "r") as puzzle_file:
        yield from (line.strip() for line in puzzle_file)


def parse_puzzle_lines(lines: Iterable[str]) -> Folder:
    lines = list(lines)[1:]
    folder = Folder(name="/")

    for i, line in enumerate(lines):
        if line.startswith("$ cd"):
            folder = change_dir(line, folder)
        if line == "$ ls":
            for item in list_directory(lines[i+1:]):
                folder.add_item(item)
    return folder.root


def change_dir(command: str, folder: Folder) -> Folder:
    requested_folder = command[5:]
    if requested_folder == "..":
        return folder.parent # type: ignore
    return folder[requested_folder] # type: ignore

def list_directory(lines: Sequence[str]) -> Sequence[Union[File, Folder]]:
    contents = takewhile(lambda line: not line.startswith("$"), lines)
    return [parse_content(content) for content in contents]

def parse_content(content: str) -> Union[File, Folder]:
    if content.startswith("dir"):
        return Folder(content[4:])
    size, name = content.split(" ")
    return File(int(size), name)

def add_to_filesystem(filesystem: dict, path: Sequence[str], items: Sequence[Union[File, Folder]]):
    target = filesystem
    for key in path:
        target = target[key]
    for item in items:
        target[item.name] = dict() if isinstance(item, Folder) else item

def solve_part_one(root: Folder) -> int:
    sizes = compute_folder_sizes(root)
    THRESHOLD = 100000
    sizes_under_limit = {key: value for key, value in sizes.items() if value <= THRESHOLD}
    return sum(sizes_under_limit.values())

def compute_folder_sizes(root: Folder) -> Dict[str, int]:
    return { folder.fullpath: folder.size for folder in (root, *root.iter_folders())}

def solve_part_two(root: Folder) -> int:
    TOTAL_SPACE = int(7 * 10e6)
    MINIMUM_FREE_SPACE = int(3 * 10e6)
    unused_space = TOTAL_SPACE - root.size
    required_space = MINIMUM_FREE_SPACE - unused_space

    sizes = compute_folder_sizes(root)
    filtered_sizes = {key: value for key, value in sizes.items() if value >= required_space}
    sorted_sizes = dict(sorted(filtered_sizes.items(), key=operator.itemgetter(1)))
    if not sorted_sizes:
        return -1
    return sorted_sizes[next(iter(sorted_sizes))]





if __name__ == '__main__':
    run_puzzle("sample_input.txt")
    run_puzzle("input.txt")
