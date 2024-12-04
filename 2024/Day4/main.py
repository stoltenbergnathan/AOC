import re
import numpy as np


def read_file(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.readlines()


def main() -> None:
    forwards: str = "XMAS"
    backwards: str = "SAMX"
    occurances: int = 0

    lines: list[str] = read_file("input.txt")

    for line in lines:
        f_matches: list[str] = re.findall(forwards, line)
        b_matches: list[str] = re.findall(backwards, line)
        occurances += len(f_matches) + len(b_matches)

    for index in range(len(lines[0]) - 1):
        vertical: str = "".join([line[index] for line in lines])
        f_matches: list[str] = re.findall(forwards, vertical)
        b_matches: list[str] = re.findall(backwards, vertical)
        occurances += len(f_matches) + len(b_matches)

    np_array = np.array([list(s.rstrip()) for s in lines])

    main_diag = np_array.diagonal()
    f_matches: list[str] = re.findall(forwards, "".join(main_diag.tolist()))
    b_matches: list[str] = re.findall(backwards, "".join(main_diag.tolist()))
    occurances += len(f_matches) + len(b_matches)

    offset: int = 1
    while True:
        diag = np_array.diagonal(offset=offset)
        if diag.shape == (0,):
            break
        f_matches: list[str] = re.findall(forwards, "".join(diag.tolist()))
        b_matches: list[str] = re.findall(backwards, "".join(diag.tolist()))
        occurances += len(f_matches) + len(b_matches)
        offset += 1

    offset: int = -1
    while True:
        diag = np_array.diagonal(offset=offset)
        if diag.shape == (0,):
            break
        f_matches: list[str] = re.findall(forwards, "".join(diag.tolist()))
        b_matches: list[str] = re.findall(backwards, "".join(diag.tolist()))
        occurances += len(f_matches) + len(b_matches)
        offset -= 1

    np_flip = np.fliplr(np_array)
    main_diag = np_flip.diagonal()
    f_matches: list[str] = re.findall(forwards, "".join(main_diag.tolist()))
    b_matches: list[str] = re.findall(backwards, "".join(main_diag.tolist()))
    occurances += len(f_matches) + len(b_matches)
    offset: int = 1
    while True:
        diag = np_flip.diagonal(offset=offset)
        if diag.shape == (0,):
            break
        f_matches: list[str] = re.findall(forwards, "".join(diag.tolist()))
        b_matches: list[str] = re.findall(backwards, "".join(diag.tolist()))
        occurances += len(f_matches) + len(b_matches)
        offset += 1

    offset: int = -1
    while True:
        diag = np_flip.diagonal(offset=offset)
        if diag.shape == (0,):
            break
        f_matches: list[str] = re.findall(forwards, "".join(diag.tolist()))
        b_matches: list[str] = re.findall(backwards, "".join(diag.tolist()))
        occurances += len(f_matches) + len(b_matches)
        offset -= 1

    print(occurances)


def part2() -> None:
    lines: list[list[str]] = [list(s.rstrip()) for s in read_file("input.txt")]

    def is_x_mas(col: int, row: int) -> bool:
        diag_1: str = ""
        diag_2: str = ""
        if (row - 1 >= 0 and row < len(lines) - 1) and (
            col - 1 >= 0 and col < len(lines[row]) - 1
        ):
            TL: str = lines[row - 1][col - 1]
            TR: str = lines[row - 1][col + 1]
            BL: str = lines[row + 1][col - 1]
            BR: str = lines[row + 1][col + 1]
            diag_1 = TL + "A" + BR
            diag_2 = TR + "A" + BL

            if (diag_1 == "MAS" or diag_1 == "SAM") and (
                diag_2 == "MAS" or diag_2 == "SAM"
            ):
                return True
        return False

    occurances: int = 0
    for row_index, row in enumerate(lines):
        for col_index, col in enumerate(row):
            if col == "A" and is_x_mas(col_index, row_index):
                occurances += 1

    print(occurances)


if __name__ == "__main__":
    part2()
