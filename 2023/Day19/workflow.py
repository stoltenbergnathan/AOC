from dataclasses import dataclass

from rule import Rule


@dataclass
class Workflow:
    name: str
    rules: list[Rule]
