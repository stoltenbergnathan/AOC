from helpers import (
  get_lowest_location_number,
  get_seeds_from_file
)

file_name: str = 'input.txt'

if __name__ == "__main__":
  seeds: list[int] = get_seeds_from_file(file_name)
  print(get_lowest_location_number(file_name, seeds))