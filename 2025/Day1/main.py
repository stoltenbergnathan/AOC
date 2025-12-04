from dataclasses import dataclass

@dataclass
class Instruction:
    direction: str
    amount: int

class Dial:
    def __init__(self) -> None:
        self._current = 50
        self.zeros_landed_on = 0
        self.zeros_passed = 0
    
    def rotate(self, direction: str, amount: int) -> int:
        prev = self._current
        self.zeros_passed += int(abs(amount) / 100)

        amount %= 100
        if direction == "L":
            self._current -= amount
        elif direction == "R":
            self._current += amount
        else:
            raise Exception("Invalid direction: " + direction)
        
        if prev != 0 and (self._current < 0 or self._current > 100):
            self.zeros_passed += 1
        
        self._current %= 100
        if self._current == 0:
            self.zeros_landed_on += 1

        return self._current

    def get_current(self) -> int:
        return self._current
    
def get_input(file: str) -> list[str]:
    with open(file) as f:
        return f.readlines()

def format_input(file_info: list[str]) -> list[Instruction]:
    instructions: list[Instruction] = []
    for line in file_info:
        direction = line[0]
        amount = int(line[1:])
        instructions.append(Instruction(direction, amount))
    return instructions

def main():
    FILE = 'input.txt'
    instructions: list[Instruction] = format_input(get_input(FILE))
    safe = Dial()
    for ins in instructions:
        old_value = safe.get_current()
        new_value = safe.rotate(ins.direction, ins.amount)
        print(f"{ins.direction}{ins.amount}: {old_value}->{new_value}")
    
    print(safe.zeros_landed_on)
    print(safe.zeros_passed)

if __name__ == "__main__":
    main()
