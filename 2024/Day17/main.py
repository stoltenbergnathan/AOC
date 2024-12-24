class Program:
    def __init__(
        self, reg_a: int, reg_b: int, reg_c: int, instructions: list[int]
    ) -> None:
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.instructions = instructions
        self.position: int = 0

    def preform_next_instruction(self) -> str:
        if self.position >= len(self.instructions):
            return "break"

        def get_combo_operand(operand: int) -> int:
            if 0 <= operand <= 3:
                return operand
            elif operand == 4:
                return self.reg_a
            elif operand == 5:
                return self.reg_b
            elif operand == 6:
                return self.reg_c

            raise Exception(f"Invalid operand for combo operand: {operand}")

        opcode: int = self.instructions[self.position]
        operand: int = self.instructions[self.position + 1]

        self.position += 2

        match opcode:
            case 0:
                numerator: int = self.reg_a
                denominator: int = pow(2, get_combo_operand(operand))
                self.reg_a = int(numerator / denominator)
            case 1:
                self.reg_b = self.reg_b ^ operand
            case 2:
                self.reg_b = get_combo_operand(operand) % 8
            case 3:
                if self.reg_a == 0:
                    pass
                else:
                    self.position = operand
            case 4:
                self.reg_b = self.reg_b ^ self.reg_c
            case 5:
                return str(get_combo_operand(operand) % 8)
            case 6:
                numerator: int = self.reg_a
                denominator: int = pow(2, get_combo_operand(operand))
                self.reg_b = int(numerator / denominator)
            case 7:
                numerator: int = self.reg_a
                denominator: int = pow(2, get_combo_operand(operand))
                self.reg_c = int(numerator / denominator)
            case e:
                raise Exception(f"Invalid opcode found: {e}")

        return f"No Output. Position: {self.position}"

    def run_program(self) -> list[int]:
        outputs: list[int] = []
        self.position = 0

        while True:
            instruction_value: str = self.preform_next_instruction()

            if instruction_value == "break":
                break
            elif "No Output" in instruction_value:
                pass
            else:
                outputs.append(int(instruction_value))

        return outputs

    def find_copy(self) -> int:
        # 2, 4, 1, 1, 7, 5, 1, 4, 0, 3, 4, 5, 5, 5, 3, 0
        # while True:
        #     o_value: str = input("Enter an octal value: ")
        #     try:
        #         self.reg_a = int("0o" + o_value, 0)
        #     except ValueError:
        #         print("Invalid value. Please try again.")

        #     outputs = self.run_program()
        #     if outputs == self.instructions:
        #         return self.reg_a

        #     print(f"Entered value: {o_value}. Outputs: {outputs}")
        pass


def read_file(filename: str) -> list[str]:
    with open(filename) as f:
        return f.readlines()


def get_reg_values(lines: list[str]) -> list[int]:
    reg_str: list[str] = lines[: lines.index("\n")]

    reg_values: list[int] = []
    for reg in reg_str:
        reg_value: int = int(reg.split(":")[1])
        reg_values.append(reg_value)

    return reg_values


def get_instructions(lines: list[str]) -> list[int]:
    instruction_str: str = lines[lines.index("\n") + 1 :][0].split(":")[1]
    return [int(instruction) for instruction in instruction_str.split(",")]


def get_program(filename: str) -> Program:
    lines: list[str] = read_file(filename)
    reg_values: list[int] = get_reg_values(lines)
    instructions: list[int] = get_instructions(lines)
    return Program(reg_values[0], reg_values[1], reg_values[2], instructions)


def main() -> None:
    FILE = "test2.txt"
    main_program: Program = get_program(FILE)
    outputs = main_program.run_program()
    print(outputs)


def main2() -> None:
    FILE = "input.txt"
    main_program: Program = get_program(FILE)
    main_program.reg_a = 0  # TOO LARGE 202943559641642
    main_program.reg_b = 0
    main_program.reg_c = 0
    print(main_program.find_copy())


def test() -> None:
    a = Program(0, 0, 9, [2, 6])
    a.run_program()
    print(f"a reg_b should be 1: {a.reg_b}")

    b = Program(10, 0, 0, [5, 0, 5, 1, 5, 4])
    b_outputs = b.run_program()
    print(f"b should output [0, 1, 2]: {b_outputs}")

    c = Program(2024, 0, 0, [0, 1, 5, 4, 3, 0])
    c_output = c.run_program()
    print(
        f"c should output [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0] and have 0 in reg_a. \nOutput{c_output}\nreg_a: {c.reg_a}"
    )

    d = Program(0, 29, 0, [1, 7])
    d.run_program()
    print(f"d reg_b should be 26: {d.reg_b}")

    e = Program(0, 2024, 43690, [4, 0])
    e.run_program()
    print(f"e reg_b should be 44354: {e.reg_b}")


if __name__ == "__main__":
    main2()
