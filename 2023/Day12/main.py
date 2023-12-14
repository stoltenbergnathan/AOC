from spring_row import SpringRow

FILE: str = "test.txt"

with open(FILE) as fs:
    lines: list[str] = fs.readlines()

total_solutions: int = 0
for line in lines:
    spring: SpringRow = SpringRow(line)
    print(f"for line: {spring.row}")

    num_valid: int = spring.get_solutions_smart()
    print(f"There exists {num_valid} solutions\n")
    total_solutions += num_valid

print(f"In total there were {total_solutions} total solutions")
