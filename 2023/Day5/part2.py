from helpers import (
  get_almanac_from_file
)
from helpers2 import (
  get_seed_sets_from_file
)

file_name = 'input.txt'

almanac = get_almanac_from_file(file_name)

test_num = 100000000
while True:
  if test_num % 1000 == 0:
    print(f"T: {test_num}")
  current_num = test_num
  for r_index in range(len(almanac.chapters) - 1, -1, -1):
    for page in almanac.chapters[r_index].pages:
      if current_num >= page.dest_start and current_num <= page.dest_start + page.range_length:
        current_num = page.source_start + (current_num - page.dest_start)
        break
  for seed_set in get_seed_sets_from_file(file_name):
    if current_num >= seed_set[0] and current_num <= seed_set[1]:
      print(test_num)
      exit(0)
  test_num += 1
