from dataclasses import dataclass
from typing import Iterable
from collections import Counter

FILE: str = "input.txt"

file_lines: list[str]
with open(FILE) as fs:
    file_lines = [line.strip() for line in fs.readlines()]


@dataclass
class MirrorBlock:
    lines: list[str]


def mirror_block_generator(file_lines: list[str]) -> Iterable[MirrorBlock]:
    block_lines: list[str] = []
    for line in file_lines:
        if line == "":
            yield MirrorBlock(block_lines)
            block_lines.clear()
        else:
            block_lines.append(line)
    yield MirrorBlock(block_lines)


def get_value(mirror_block: MirrorBlock) -> int:
    middle_point: int = int(len(mirror_block.lines) / 2)
    outsiders: list[str] = [k for k, v in Counter(mirror_block.lines).items() if v == 1]
    if len(outsiders) == 1:
        outsider_index: int = mirror_block.lines.index(outsiders[0])
        if outsider_index > middle_point:
            # print(f"{outsiders[0]} is below the flip index")
            return middle_point
        else:
            # print(f"{outsiders[0]} is above the flip index")
            return (1 + middle_point) * 100

    mirror_block.lines = list(zip(*mirror_block.lines))
    middle_point: int = int(len(mirror_block.lines) / 2)
    outsiders: list[str] = [k for k, v in Counter(mirror_block.lines).items() if v == 1]
    if len(outsiders) == 1:
        outsider_index: int = mirror_block.lines.index(outsiders[0])
        if outsider_index > middle_point:
            # print(f"{outsiders[0]} is left of the flip index")
            return middle_point
        else:
            # print(f"{outsiders[0]} is right of the flip index")
            return 1 + middle_point
    raise Exception("*shrug*")


def main() -> None:
    print(
        [get_value(mirror_block) for mirror_block in mirror_block_generator(file_lines)]
    )


if __name__ == "__main__":
    main()
