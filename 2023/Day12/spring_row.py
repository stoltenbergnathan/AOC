from itertools import product
from typing import Iterable


class SpringRow:
    def __init__(self, spring_row: str) -> None:
        self.spring_row: str = spring_row.strip()
        self.damaged_groups: list[int] = []
        self.row: str
        self.parse_spring_row()

    def parse_spring_row(self) -> None:
        space_split: list[str] = self.spring_row.split()

        self.row = space_split[0]
        # copy_row: str = self.row
        # for _ in range(4):
        #     self.row += "?"
        #     self.row += copy_row

        for num in space_split[1].split(","):
            self.damaged_groups.append(int(num))

        # copy_damaged: list[int] = self.damaged_groups.copy()
        # for _ in range(4):
        #     self.damaged_groups.extend(copy_damaged)

    def generate_possible_solutions(self) -> Iterable[str]:
        for combo in product(".#", repeat=self.row.count("?")):
            possible_solution: str = ""
            combo_index: int = 0
            for char in self.row:
                if char == "?":
                    possible_solution += combo[combo_index]
                    combo_index += 1
                else:
                    possible_solution += char
            yield possible_solution

    def number_of_valid_solutions(self) -> int:
        num_solutions: int = 0
        for possible_solution in self.generate_possible_solutions():
            if self.is_valid_solution(possible_solution):
                num_solutions += 1
        return num_solutions

    def is_valid_solution(self, solution: str) -> bool:
        in_damaged: bool = False
        groupings_left: list[int] = self.damaged_groups.copy()
        damaged_length: int = 0
        for char in solution + ".":
            if char == "#" and in_damaged:
                damaged_length += 1
            elif char == "#":
                in_damaged = True
                damaged_length = 1
            elif in_damaged and char == ".":
                if len(groupings_left) > 0 and damaged_length == groupings_left[0]:
                    groupings_left.remove(damaged_length)
                    in_damaged = False
                else:
                    return False
        if len(groupings_left) == 0:
            return True
        return False

    def get_solutions_smart(self) -> int:
        raise NotImplementedError
