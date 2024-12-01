from dataclasses import dataclass

@dataclass
class Page:
  dest_start: int
  source_start: int
  range_length: int

@dataclass
class Chapter:
  pages: list[Page]

@dataclass
class Almanac:
  chapters: list[Chapter]

def get_lines_from_file(file_name: str) -> list[str]:
  with open(file_name) as fs:
    return fs.readlines()

def get_seeds_from_file(file_name: str) -> list[int]:
  lines: list[str] = get_lines_from_file(file_name)
  return [int(num) for num in lines[0][6:].split()]

def get_almanac_from_file(file_name: str) -> Almanac:
  lines: list[str] = get_lines_from_file(file_name)
  chapters: list[Chapter] = []

  new_chapter: bool = True
  for line in lines[1:]:
    if line == '\n':
      new_chapter = True
      continue

    if new_chapter:
      new_chapter = False
      chapters.append(Chapter(pages=[]))
    
    if ':' in line:
      continue

    page_info: list[str] = line.split()
    dest_start: int = int(page_info[0])
    source_start: int = int(page_info[1])
    range_length: int = int(page_info[2])

    chapters[-1].pages.append(Page(dest_start, source_start, range_length))

  return Almanac(chapters)

def process_seed(seed: int, almanac: Almanac) -> int:
  start_value: int = seed
  end_value: int = seed
  for chapter in almanac.chapters:
    for page in chapter.pages:
      if start_value in range(page.source_start, page.source_start + page.range_length):
        end_value = page.dest_start + (start_value - page.source_start)
        break
    start_value = end_value
  return end_value


def get_lowest_location_number(input_file: str, seeds: list[int]) -> int:
  almanac = get_almanac_from_file(input_file)

  locations: list[int] = []
  for seed in seeds:
    locations.append(process_seed(seed, almanac))
  
  return min(locations)
