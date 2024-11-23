from enum import Enum


class Pulse(Enum):
    low = 0
    high = 1


class State(Enum):
    unknown = -1
    off = 0
    on = 1

    def toggle(self) -> "State":
        if self == State.off:
            return State.on
        return State.off


class Module:
    def __init__(self, name: str, destination_modules: list["Module"]) -> None:
        self.name = name
        self.destination_modules = destination_modules

    def input(self, pulse: Pulse, sending_module: "Module") -> None:
        pass


class FlipFlop(Module):
    def __init__(self, name: str, destination_modules: list[Module]) -> None:
        super().__init__(name, destination_modules)
        self.state: State = State.off

    def input(self, pulse: Pulse, sending_module: Module):
        if pulse == Pulse.high:
            return

        pulse_to_send: Pulse
        if self.state == State.off:
            pulse_to_send = Pulse.high
        else:
            pulse_to_send = Pulse.low

        self.state = self.state.toggle()

        for module in self.destination_modules:
            module.input(pulse_to_send, self)


class Conjunction(Module):
    def __init__(self, name: str, destination_modules: list[Module]) -> None:
        super().__init__(name, destination_modules)
        self.state: State = State.unknown
        self.last_pulse_from_desitnations: dict[Module, Pulse]
        for module in self.destination_modules:
            self.last_pulse_from_desitnations[module] = Pulse.low

    def input(self, pulse: Pulse, sending_module: Module):
        self.last_pulse_from_desitnations[sending_module] = pulse

        pulse_to_send: Pulse
        if self.last_pulse_from_desitnations.values().__contains__(Pulse.low):
            pulse_to_send = Pulse.high
        else:
            pulse_to_send = Pulse.low

        for module in self.destination_modules:
            module.input(pulse_to_send, self)


class Broadcaster(Module):
    def __init__(self, name: str, destination_modules: list[Module]) -> None:
        super().__init__(name, destination_modules)

    def input(self, pulse: Pulse, sending_module: Module) -> None:
        for module in self.destination_modules:
            module.input(pulse, self)


def get_init_modules_from_input() -> list[Module]:
    lines: list[str]
    found_modules: list[Module] = []
    with open("./input.txt") as f:
        lines = f.readlines()

    for line in lines:
        splits: list[str] = line.split("->")
        input_module: str = splits[0].replace(" ", "")
        new_module: Module

        if input_module == "broadcaster":
            new_module = Broadcaster(input_module, [])
        elif input_module.startswith("%"):
            new_module = FlipFlop(input_module.lstrip("%"), [])
        elif input_module.startswith("&"):
            new_module = Conjunction(input_module.lstrip("&"), [])
        else:
            raise Exception("Cannot convert into a module: ", input_module)

        found_modules.append(new_module)

    return found_modules


if __name__ == "__main__":
    mods = get_init_modules_from_input()
    for mod in mods:
        print(mod.name + " " + str(type(mod)))
