from enum import Enum
import sys

sys.setrecursionlimit(1000000000)

FILE_NAME: str = 'input.txt'
PART2: bool = True

pipe_map: list[list[str]] = []

STARTING_CHAR: str = 'S'
GROUND_CHAR: str = '.'

class PipeType(Enum):
  vertical = '|'
  horizontal = '-'
  north_east = 'L'
  north_west = 'J'
  south_west = '7'
  south_east = 'F'


class Direction(Enum):
  north = 0
  south = 1
  east = 2
  west = 3

direction_pipe_mapping: dict[tuple[PipeType, Direction], tuple[tuple[int, int], Direction]] = {
  (PipeType.vertical, Direction.north): ((-1, 0), Direction.north),
  (PipeType.vertical, Direction.south): ((1, 0), Direction.south),
  (PipeType.horizontal, Direction.east): ((0, 1), Direction.east),
  (PipeType.horizontal, Direction.west): ((0, -1), Direction.west),
  (PipeType.north_east, Direction.south): ((0, 1), Direction.east),
  (PipeType.north_east, Direction.west): ((-1, 0), Direction.north),
  (PipeType.north_west, Direction.south): ((0, -1), Direction.west),
  (PipeType.north_west, Direction.east): ((-1, 0), Direction.north),
  (PipeType.south_west, Direction.north): ((0, -1), Direction.west),
  (PipeType.south_west, Direction.east): ((1, 0), Direction.south),
  (PipeType.south_east, Direction.north): ((0, 1), Direction.east),
  (PipeType.south_east, Direction.west): ((1, 0), Direction.south),
}


def fill_pipe_map(pipe_map: list[list[str]]) -> None:
  with open(FILE_NAME) as fs:
    lines = fs.readlines()
  
  for line in lines:
    char_line: list[str] = []
    for char in line:
      char_line.append(char)
    pipe_map.append(char_line)

def get_starting_pipe(current_location: tuple[int, int]) -> tuple[tuple[int, int], Direction]:
  if pipe_map[current_location[0] - 1][current_location[1]] in [PipeType.vertical.value, PipeType.south_east.value, PipeType.south_west.value]:
    return ((current_location[0] - 1, current_location[1]), Direction.north)
  elif pipe_map[current_location[0] + 1][current_location[1]] in [PipeType.vertical.value, PipeType.north_east.value, PipeType.north_west.value]:
    return ((current_location[0] + 1, current_location[1]), Direction.south)
  elif pipe_map[current_location[0]][current_location[1] - 1] in [PipeType.horizontal.value, PipeType.north_east.value, PipeType.south_east.value]:
    return ((current_location[0], current_location[1] - 1), Direction.west)
  elif pipe_map[current_location[0]][current_location[1] + 1] in [PipeType.horizontal.value, PipeType.north_west.value, PipeType.north_west.value]:
    return ((current_location[0], current_location[1] + 1), Direction.east)
  else:
    raise Exception("Could not find a starting location")

def get_next_pipe(current_location: tuple[int, int], direction: Direction | None = None) -> tuple[tuple[int, int], Direction]:
  if direction == None:
    return get_starting_pipe(current_location)
  
  next_values: tuple[tuple[int, int], Direction] = direction_pipe_mapping[PipeType(pipe_map[current_location[0]][current_location[1]]), direction]
  next_location: tuple[int, int] = (current_location[0] + next_values[0][0], current_location[1] + next_values[0][1])
  return (next_location, next_values[1])


def find_starting_location(pipe_map: list[list[str]]) -> tuple[int, int]:
  for (row_index, row) in enumerate(pipe_map):
    if STARTING_CHAR in row:
      return (row_index, row.index(STARTING_CHAR))
  raise Exception(f"{STARTING_CHAR} not found in pipe_map")

def follow_pipes(location: tuple[tuple[int, int], Direction | None], steps: int, starting: bool = False) -> int:
  if pipe_map[location[0][0]][location[0][1]] == STARTING_CHAR and not starting:
    return steps
  
  next_pipe_location: tuple[tuple[int, int], Direction] = get_next_pipe(location[0], location[1])
  steps += 1

  return follow_pipes(next_pipe_location, steps)

def main() -> None:
  fill_pipe_map(pipe_map)
  starting_location: tuple[int, int] = find_starting_location(pipe_map)
  farthest_pipe_distance: int = int(follow_pipes((starting_location, None), 0, True) / 2)
  print(farthest_pipe_distance)
 
if __name__ == "__main__":
  main()
