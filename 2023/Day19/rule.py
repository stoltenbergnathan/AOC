from dataclasses import dataclass
from part_category import PartCategory


@dataclass
class Rule:
    part_category: PartCategory | None
    condition: str | None
    value: int | None
    next_step: str
