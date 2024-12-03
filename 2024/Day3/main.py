from dataclasses import dataclass


@dataclass
class MULInstruction:
    x: int
    y: int


def read_file(file_name: str) -> str:
    with open(file_name) as f:
        return f.read()


def parse_lines(lines: str) -> list[MULInstruction]:
    instructions: list[MULInstruction] = []
    DO: str = "do()"
    DONT: str = "don't()"
    enabled: bool = True
    begining_mul: str = "mul("
    previous_index: int = 0
    current_index: int = lines.find(begining_mul)

    while current_index != -1:
        if DONT in lines[previous_index:current_index]:
            enabled = False
        elif DO in lines[previous_index:current_index]:
            enabled = True

        on_x: bool = True
        x: int
        x_str: str = ""
        y: int
        y_str: str = ""
        valid: bool = True
        distance_covered: int = 0
        for sub_index in range(4, 12):
            distance_covered += 1
            current_char: str = lines[current_index + sub_index]
            if current_char.isdigit():
                if on_x:
                    x_str += current_char
                else:
                    y_str += current_char
            elif current_char == "," and on_x == True:
                on_x = False
                continue
            elif current_char == ")" and (x_str != "" and y_str != ""):
                break
            else:
                valid = False
                break
        if valid and enabled:
            x = int(x_str)
            y = int(y_str)
            instruction: MULInstruction = MULInstruction(x, y)
            instructions.append(instruction)

        previous_index = current_index
        current_index = lines.find(begining_mul, current_index + distance_covered)

    return instructions


def main() -> None:
    FILE_NAME = "input.txt"
    file: str = read_file(FILE_NAME)
    instructions: list[MULInstruction] = parse_lines(file)
    final_value: int = 0
    for instruction in instructions:
        final_value += instruction.x * instruction.y
    print(final_value)


if __name__ == "__main__":
    main()
