'''
# Tried async, but still took too long
# async def iterate_seeds(start: int, end: int) -> list[int]:
#   return [seed for seed in range(start, end)]

# async def get_seeds_from_seed_group(
#     seed_start: int,
#     seed_end: int
#   ) -> list[int]:
#   seeds: list[int] = []

#   async with asyncio.TaskGroup() as tg:
#       task1: asyncio.Task[list[int]] = tg.create_task(iterate_seeds(seed_start, int((seed_start + seed_end) / 2)))
#       task2: asyncio.Task[list[int]] = tg.create_task(iterate_seeds(int((seed_start + seed_end) / 2), seed_end))
  
#   seeds.extend(task1.result())
#   seeds.extend(task2.result())
  
#   return seeds

# async def get_seeds_from_file_pt2(file_name: str) -> list[int]:
#   seed_line: list[str] = get_lines_from_file(file_name)[0][6:].split()
#   seeds: list[int] = []
#   tasks: list[asyncio.Task[list[int]]] = []
#   async with asyncio.TaskGroup() as tg:
#     for (index, seed_start) in enumerate(seed_line):
#       seed_start = int(seed_start)
#       if index % 2 != 0:
#         continue
#       tasks.append(
#         tg.create_task(
#           get_seeds_from_seed_group(
#             seed_start, seed_start + int(seed_line[index + 1])
#           )
#         )
#       )
  
  
#   for task in tasks:
#     seeds.extend(task.result())
  
#   return seeds

def seed_splits_generator(input_file: str) -> Iterator[tuple[int, int]]:
  STEP: int = 100
  with open(input_file) as fs:
    seed_line: str = fs.readline()
  seeds: list[str] = seed_line[6:].split()
  for index in range(0, len(seeds), 2):
    range_len: int = int(seeds[index + 1])
    start: int = int(seeds[index])
    end: int = 0
    while range_len != 0:
      if range_len - STEP > 0:
        end = start + STEP
        range_len -= STEP
        yield (start, end)
      else:
        end = int(seeds[index]) + int(seeds[index + 1])
        yield(start, end)
        break
      start = end

def seed_generator(input_file: str) -> Iterator[int]:
  with open(input_file) as fs:
    seed_line: str = fs.readline()
  seeds: list[str] = seed_line[6:].split()
  for index in range(0, len(seeds), 2):
    print(f"Processing seed range: {index}")
    for seed in range(int(seeds[index]), int(seeds[index]) + int(seeds[index + 1])):
      if seed == int(int(seeds[index]) + int(seeds[index]) + int(seeds[index + 1]) / 2):
        print(f"Halfway for seed range: {index}")
      yield seed
'''

from typing import Iterator


def get_seed_sets_from_file(file_name: str) -> Iterator[tuple[int, int]]:
  with open(file_name) as fs:
    seed_line: str = fs.readline()
  seeds: list[str] = seed_line[6:].split()
  for index in range(0, len(seeds), 2):
    yield (int(seeds[index]), int(seeds[index]) + int(seeds[index + 1]))
