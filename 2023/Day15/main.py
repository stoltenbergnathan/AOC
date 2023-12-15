from dataclasses import dataclass
from enum import Enum

FILE: str = "input.txt"
PART2: bool = True
with open(FILE) as fs:
    raw_line: str = fs.readline().strip()


class Operation(Enum):
    ADD = "="
    SUBTRACT = "-"


@dataclass
class Sequence:
    label: str
    focal_length: int
    operation: Operation


init_seq: list[Sequence] = []
for line in raw_line.split(","):
    label: str
    oper: Operation
    focal_length: int
    if "-" in line:
        oper = Operation.SUBTRACT
        label = line.split(oper.value)[0]
        focal_length = -1
    else:
        oper = Operation.ADD
        label = line.split(oper.value)[0]
        focal_length = int(line.split(oper.value)[1])
    init_seq.append(Sequence(label, focal_length, oper))

if not PART2:
    running_sum: int = 0
    for seq in init_seq:
        currnet_value: int = 0
        for char in seq.label + seq.operation.value + str(seq.focal_length):
            # Determine the ASCII code for the current character of the string.
            ascii_value: int = ord(char)

            # Increase the current value by the ASCII code you just determined.
            currnet_value += ascii_value

            # Set the current value to itself multiplied by 17.
            currnet_value *= 17

            # Set the current value to the remainder of dividing itself by 256.
            currnet_value %= 256
        running_sum += currnet_value
    print(running_sum)
else:
    hashmap: dict[int, list[Sequence]] = {}
    for seq in init_seq:
        currnet_value: int = 0
        for char in seq.label:
            # Determine the ASCII code for the current character of the string.
            ascii_value: int = ord(char)

            # Increase the current value by the ASCII code you just determined.
            currnet_value += ascii_value

            # Set the current value to itself multiplied by 17.
            currnet_value *= 17

            # Set the current value to the remainder of dividing itself by 256.
            currnet_value %= 256

        label_in_hash: bool = currnet_value in hashmap
        if seq.operation == Operation.ADD:
            if label_in_hash:
                found: bool = False
                for a_seq in hashmap[currnet_value]:
                    if a_seq.label == seq.label:
                        a_seq.focal_length = seq.focal_length
                        found = True
                if not found:
                    hashmap[currnet_value].append(seq)
            else:
                hashmap[currnet_value] = [seq]
        else:
            if not label_in_hash:
                continue
            else:
                for a_seq in hashmap[currnet_value]:
                    if a_seq.label == seq.label:
                        hashmap[currnet_value].remove(a_seq)

    final_answer: int = 0
    for box_num, lenses in hashmap.items():
        for index, lens in enumerate(lenses):
            final_answer += (box_num + 1) * (index + 1) * lens.focal_length
    print(final_answer)
