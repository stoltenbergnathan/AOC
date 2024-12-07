from itertools import product

PART2: bool = True


class Equation:
    def __init__(self, line: str) -> None:
        split: list[str] = line.split(":")
        self.answer: int = int(split[0])
        self.numbers: list[int] = [int(num) for num in split[1].split()]

    def generate_operations(self) -> list[tuple[str, ...]]:
        operations: list[str] = ["+", "*"]
        if PART2:
            operations.append("||")
        return list(product(operations, repeat=len(self.numbers) - 1))

    def generate_combonations(self) -> list[str]:
        combonations: list[str] = []
        operations: list[tuple[str, ...]] = self.generate_operations()

        for operation in operations:
            equation: str = str(self.numbers[0])
            for i in range(1, len(self.numbers)):
                equation += f" {operation[i - 1]} {self.numbers[i]}"

            combonations.append(equation)

        return combonations

    def is_solvable(self) -> bool:
        equation_combonations: list[str] = self.generate_combonations()

        for permutation in equation_combonations:
            if self.solve_permutation(permutation) == self.answer:
                return True

        return False

    def solve_permutation(self, permutation: str) -> int:
        permutation_split: list[str] = permutation.split()

        result: str = permutation_split[0]
        for i in range(1, len(permutation_split), 2):
            if permutation_split[i] == "+":
                result = str(int(result) + int(permutation_split[i + 1]))
            elif permutation_split[i] == "*":
                result = str(int(result) * int(permutation_split[i + 1]))
            elif permutation_split[i] == "||":
                result = result + str(self.solve_permutation(permutation_split[i + 1]))

        return int(result)


def read_input(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.readlines()


def main() -> None:
    lines: list[str] = read_input("input.txt")

    equations: list[Equation] = []
    for line in lines:
        equations.append(Equation(line))

    solvable: list[Equation] = []
    for equation in equations:
        if equation.is_solvable():
            solvable.append(equation)

    print("Found {} solvable equations".format(len(solvable)))

    total: int = 0
    for equation in solvable:
        total += equation.answer

    print("Total: {}".format(total))


if __name__ == "__main__":
    main()
