from dataclasses import dataclass
from enum import Enum
from math import lcm

class Direction(Enum):
  LEFT = "L"
  RIGHT = "R"

@dataclass
class Split:
  left: str
  right: str


file_name: str = "input.txt"

with open(file_name) as fs:
  lines = fs.readlines()

instructions: list[str] = [*lines[0].strip()]
map_dict: dict[str, Split] = {}
for node in lines[2:]:
  node_split: list[str] = node.split(' = ')
  current_node: str = node_split[0]
  current_split: list[str] = node_split[1].replace('(', '').replace(')', '').strip().split(', ')
  map_dict[current_node] = Split(current_split[0], current_split[1])


class Ghost:
  def __init__(self, starting_node: str) -> None:
    self.current_node = starting_node
    self.path_taken: list[str] = [starting_node]
  
  def move(self, direction: Direction) -> None:
    if direction == Direction.LEFT:
      self.current_node = map_dict[self.current_node].left
    else:
      self.current_node = map_dict[self.current_node].right
    
    self.path_taken.append(self.current_node)
  
  def end_in_z(self) -> bool:
    if self.current_node[-1] == 'Z':
      return True
    return False
  
  

def part1() -> None:
  print("Starting at AAA")
  instruction_index: int = 0
  steps: int = 0
  current_node: str = 'AAA'
  end_node: str = 'ZZZ'
  while True:
    if instructions[instruction_index] == Direction.LEFT.value:
      current_node = map_dict[current_node].left
    else:
      current_node = map_dict[current_node].right
    
    steps += 1
    if instruction_index < len(instructions) - 1:
      instruction_index += 1
    else:
      instruction_index = 0
    
    if current_node == end_node:
      print(f"It took {steps} steps to reach ZZZ from AAA")
      break

def part2_brute() -> None:
  ghosts: list[Ghost] = []
  for node in map_dict.keys():
    if node[-1] == 'A':
      ghosts.append(Ghost(node))
  
  steps: int = 0
  instruction_index: int = 0
  while True:
    for ghost in ghosts:
      ghost.move(Direction(instructions[instruction_index]))
    
    steps += 1
    print(steps)
    if instruction_index < len(instructions) - 1:
      instruction_index += 1
    else:
      instruction_index = 0
    
    for ghost in ghosts:
      if ghost.end_in_z():
        break

def part2_lcm() -> None:
  ghosts: list[Ghost] = []
  for node in map_dict.keys():
    if node[-1] == 'A':
      ghosts.append(Ghost(node))
  
  steps: int = 0
  instruction_index: int = 0
  steps_to_z: list[int] = []
  while True:
    for ghost in ghosts:
      ghost.move(Direction(instructions[instruction_index]))
    
    steps += 1
    if instruction_index < len(instructions) - 1:
      instruction_index += 1
    else:
      instruction_index = 0
    
    for ghost in ghosts:
      if ghost.end_in_z():
        steps_to_z.append(steps)
        ghosts.remove(ghost)
    if len(ghosts) == 0:
      break

  print(lcm(*steps_to_z))


if __name__ == "__main__":
  part2_lcm()