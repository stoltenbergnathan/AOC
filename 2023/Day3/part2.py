from part1 import (
  EngineSchematic
)

schematic_matrix: list[list[str]] = [[]]

def get_gear_ratio(row_index: int, col_index: int) -> int:
  """
  Args:
      row_index (int): the row in the matrix of the gear
      col_index (int): the col in the matrix of the gear

  Returns:
      int: The gear ratio for the row and col provided or -1 if there was no viable ratio
  """
  offsets = [-1, 0, 1]
  ratios = []
  for row_offset in offsets:
    in_digit: bool = False
    for col_offset in offsets:
      try:
        value = schematic_matrix[row_index + row_offset][col_index + col_offset]
      except IndexError:
        value = "."

      if value.isdigit():
        if not in_digit:
          in_digit = True
          ratios.append(find_full_number(row_index + row_offset, col_index + col_offset))
      else:
        in_digit = False
  if len(ratios) < 2:
    return -1
  elif len(ratios) == 2:
    return ratios[0] * ratios[1]
  else:
    raise Exception(f"Found 3 number near a gear on row {row_index}, col {col_index}")
  

def find_full_number(row_index: int, col_index: int) -> int:
  """Finds the full number given a row and col index

  Args:
      row_index (int): the row in the matrix of the found number
      col_index (int): the col in the matrix of the found number

  Returns:
      int: the full number based on the index of the digit
  """  
  while True:
    try:
      value = schematic_matrix[row_index][col_index - 1]
    except:
      value = '.'
    if value.isdigit():
      col_index -= 1
    else:
      break
  
  num: str = ''
  while True:
    try:
      value = schematic_matrix[row_index][col_index]
    except:
      value = '.'
    if value.isdigit():
      num += value
      col_index += 1
    else:
      break
  
  return int(num)
      

  

if __name__ == "__main__":
  e = EngineSchematic('input.txt')
  schematic_matrix = e.schematic_matrix
  total: list[int] = []
  for (row, _) in enumerate(schematic_matrix):
    for (col, _) in enumerate(schematic_matrix):
      if schematic_matrix[row][col] == '*':
        ratio = get_gear_ratio(row, col)
        if ratio != -1:
          total.append(ratio)
  print(sum(total))
