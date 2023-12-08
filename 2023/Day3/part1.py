from enum import Enum
class NumberStatus(Enum):
  FIRST = 0
  LAST = 1
  NEITHER = 2

class PartNumber:
  def __init__(
      self,
      line_index: int,
      first_number_index: int,
      schematic_matrix: list[list[str]]) -> None:
    self.line_index: int = line_index
    self.first_number_index: int = first_number_index
    self.schematic_matrix: list[list[str]] = schematic_matrix
    self.full_number: int = -1
  
  def is_valid(self) -> bool:
    digit = f""
    valid = True
    status: NumberStatus = NumberStatus.FIRST
    for (char_index, char) in enumerate(self.schematic_matrix[self.line_index][self.first_number_index:]):
      if char.isdigit():
        if not self.check_validness(char_index + self.first_number_index, status):
          valid = False
        digit += char
        status = NumberStatus.NEITHER
      else:
        self.full_number = int(digit)
        if not self.check_validness(char_index + self.first_number_index - 1, NumberStatus.LAST):
          valid = False
        break
    self.full_number = int(digit)
    return valid
  
  def check_validness(self, char_index: int, number_status: NumberStatus) -> bool:
    if number_status == NumberStatus.FIRST:
      if char_index != 0:
        if not self.check_column(char_index - 1):
          return False
    elif number_status == NumberStatus.LAST:
      if char_index < len(self.schematic_matrix[self.line_index]):
        if not self.check_column(char_index + 1):
          return False

    return self.check_column(char_index)
  
  def check_column(self, char_index: int) -> bool:
    if self.line_index != 0:
      currnet_char = self.schematic_matrix[self.line_index - 1][char_index]
      if not currnet_char.isdigit() and currnet_char != '.':
        return False
      
    # To please Colin's phat ego, include a check here to not check the number itself
    currnet_char = self.schematic_matrix[self.line_index][char_index]
    if not currnet_char.isdigit() and currnet_char != '.':
      return False
    
    if self.line_index + 1 < len(self.schematic_matrix):
      currnet_char = self.schematic_matrix[self.line_index + 1][char_index]
      if not currnet_char.isdigit() and currnet_char != '.':
        return False
    
    return True



class EngineSchematic:
  def __init__(self, file_name: str) -> None:
    self.file_name: str = file_name
    self.schematic_matrix: list[list[str]] = []
    self.build_schematic_matrix(self.get_lines_from_file())
  
  def get_lines_from_file(self) -> list[str]:
    with open(self.file_name) as fs:
      return fs.readlines()

  def build_schematic_matrix(self, schematic_lines: list[str]) -> None:
    for line in schematic_lines:
      line = line.strip('\n')
      placeholder = []
      for char in line:
        placeholder.append(char)
      self.schematic_matrix.append(placeholder)
  
  def get_part_number_sum(self) -> int:
    correct_part_numbers: list[int] = []
    for (line_index, line) in enumerate(self.schematic_matrix):
      valid_numbers = self.grab_valid_parts(line_index, line)
      correct_part_numbers.extend(valid_numbers)
    return sum(correct_part_numbers)

  def grab_valid_parts(self, line_index: int, line: list[str]) -> list[int]:
    part_numbers: list[PartNumber] = []
    in_digit = False
    for (char_index, char) in enumerate(line):
      if char.isdigit():
        if not in_digit:
          part_numbers.append(PartNumber(line_index, char_index, self.schematic_matrix))
          in_digit = True
      else:
        in_digit = False
    
    # DEBUGGIN
    r_list = []
    for part in part_numbers:
      valid = not part.is_valid()
      if not valid:
        print(f"Part: {part.full_number} is not valid")
      else:
        r_list.append(part.full_number)
    return r_list
    
if __name__ == "__main__":
  e = EngineSchematic('input.txt')
  print(e.get_part_number_sum())
