from part import Part
from workflow import Workflow


class System:
    def __init__(self, workflows: list[Workflow]) -> None:
        self.workflows: list[Workflow] = workflows
        self.start: Workflow = list(
            filter(lambda workflow: workflow.name == "in", self.workflows)
        )[0]

    def part_passes(self, part: Part) -> bool:
        current_workflow: Workflow = self.start

        while True:
            for rule in current_workflow.rules:
                if rule.part_category == None:
                    if rule.next_step == "A":
                        return True
                    elif rule.next_step == "R":
                        return False
                    else:
                        for w in self.workflows:
                            if w.name == rule.next_step:
                                current_workflow = w
                        break

                q: int = int(part.__getattribute__(rule.part_category.value))
                if eval(f"{q} {rule.condition} {rule.value}"):
                    if rule.next_step == "A":
                        return True
                    elif rule.next_step == "R":
                        return False
                    else:
                        for w in self.workflows:
                            if w.name == rule.next_step:
                                current_workflow = w
                        break
