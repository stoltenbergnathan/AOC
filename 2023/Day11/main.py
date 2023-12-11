from universe import Universe

FILE_NAME: str = 'input.txt'
universe_image: list[list[str]] = []
with open(FILE_NAME) as fs:
  for line in fs.readlines():
    universe_image.append([char for char in line.strip()])

# PART1 is 1, PART2 is 999999
u = Universe(universe_image, 999999)
print(u.get_sum_of_path_between_pairs())