from galaxy import Galaxy
from itertools import combinations

class Universe:
  def __init__(self, image: list[list[str]], space_expansion: int) -> None:
    self.image: list[list[str]] = image
    self.SPACE_EXPANSION: int = space_expansion
    self.row_gaps: list[int] = []
    self.col_gaps: list[int] = []
    self.grow_universe()

    self.galaxies: list[Galaxy] = []
    self.find_galaxies()
  
  def grow_universe(self) -> None:
    for (index, row) in enumerate(self.image):
      if len(row) == row.count("."):
        self.row_gaps.append(index)
    
    # Temporarily transpose the matrix to work with columns
    self.image = list(map(list, zip(*self.image)))

    for (index, col) in enumerate(self.image):
      if len(col) == col.count("."):
        self.col_gaps.append(index)
    
    # Bring the matrix back to normal
    self.image = list(map(list, zip(*self.image)))
    self.image = list(map(list, zip(*self.image)))
    self.image = list(map(list, zip(*self.image)))

  def find_galaxies(self) -> None:
    for (r_index, row) in enumerate(self.image):
      for (c_index, col) in enumerate(row):
        if col == "#":
          self.galaxies.append(Galaxy(r_index, c_index))

  def get_sum_of_path_between_pairs(self) -> int:
    shortest_paths: list[int] = []
    for combo in combinations(self.galaxies, 2):
      num_empty_rows: int = len([value for value in range(combo[0].row, combo[1].row) if value in self.row_gaps])
      num_empty_cols: int = len([value for value in range(min(combo[0].col, combo[1].col), max(combo[1].col, combo[0].col)) if value in self.col_gaps])
      shortest_paths.append(abs(combo[1].row - combo[0].row) + abs(combo[1].col - combo[0].col) + (num_empty_cols * self.SPACE_EXPANSION) + (num_empty_rows * self.SPACE_EXPANSION))
    return sum(shortest_paths)
