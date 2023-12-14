FILE: str = "input.txt"

with open(FILE) as fs:
    file_lines: list[str] = [line.strip() for line in fs.readlines()]

rock_matrix: list[list[str]] = []

for line in file_lines:
    rock_matrix.append([char for char in line])


def move_rock_north(row: int, col: int) -> None:
    while True:
        try:
            if row != 0 and rock_matrix[row - 1][col] == ".":
                rock_matrix[row][col] = "."
                rock_matrix[row - 1][col] = "O"
                row -= 1
            else:
                break
        except:
            break


for r_index, row in enumerate(rock_matrix):
    for c_index, col in enumerate(row):
        if col == "O":
            move_rock_north(r_index, c_index)

weight_scale: int = 1
total_load: int = 0
for r_index in range(len(rock_matrix) - 1, -1, -1):
    total_load += weight_scale * rock_matrix[r_index].count("O")
    weight_scale += 1

print(total_load)
