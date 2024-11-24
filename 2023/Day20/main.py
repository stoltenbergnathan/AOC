from enum import Enum
from typing import Tuple

low_pulses_sent: int = 0
high_pulses_sent: int = 0

num_butt_pressed: int = 0


class ModuleQueue:
    queue: list[Tuple["Module", "Pulse", "Module"]] = []

    @classmethod
    def add(cls, mod: "Module", pulse: "Pulse", parent: "Module") -> None:
        cls.queue.append((mod, pulse, parent))

    @classmethod
    def take(cls) -> Tuple["Module", "Pulse", "Module"] | None:
        if len(cls.queue) != 0:
            return cls.queue.pop(0)
        return None


class Pulse(Enum):
    low = 0
    high = 1


def count_pulse(pulse: Pulse) -> None:
    global high_pulses_sent
    global low_pulses_sent

    if pulse == Pulse.high:
        high_pulses_sent += 1
    else:
        low_pulses_sent += 1


class State(Enum):
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
        if self.name == "df" and pulse == Pulse.high and sending_module.name == "xl":
            print("BREAK: ", num_butt_pressed)
            exit()
        # print(sending_module.name + " -" + pulse.name + "-> " + self.name)


class FlipFlop(Module):
    def __init__(self, name: str, destination_modules: list[Module]) -> None:
        super().__init__(name, destination_modules)
        self.state: State = State.off

    def input(self, pulse: Pulse, sending_module: Module):
        super().input(pulse, sending_module)

        if pulse == Pulse.high:
            return

        pulse_to_send: Pulse
        if self.state == State.off:
            pulse_to_send = Pulse.high
        else:
            pulse_to_send = Pulse.low

        self.state = self.state.toggle()

        for module in self.destination_modules:
            count_pulse(pulse_to_send)
            ModuleQueue.add(module, pulse_to_send, self)


class Conjunction(Module):
    def __init__(self, name: str, destination_modules: list[Module]) -> None:
        super().__init__(name, destination_modules)
        self.last_pulse_from_desitnations: dict[Module, Pulse] = {}

    def input(self, pulse: Pulse, sending_module: Module):
        super().input(pulse, sending_module)

        self.last_pulse_from_desitnations[sending_module] = pulse

        pulse_to_send: Pulse
        if Pulse.low in self.last_pulse_from_desitnations.values():
            pulse_to_send = Pulse.high
        else:
            pulse_to_send = Pulse.low

        for module in self.destination_modules:
            count_pulse(pulse_to_send)
            ModuleQueue.add(module, pulse_to_send, self)


class Broadcaster(Module):
    def __init__(self, name: str, destination_modules: list[Module]) -> None:
        super().__init__(name, destination_modules)

    def input(self, pulse: Pulse, sending_module: Module) -> None:
        super().input(pulse, sending_module)

        for module in self.destination_modules:
            count_pulse(pulse)
            ModuleQueue.add(module, pulse, self)


def get_modules_from_input() -> list[Module]:
    lines: list[str]
    modules: dict[Module, list[str]] = {}
    with open("./input.txt") as f:
        lines = f.readlines()

    for line in lines:
        splits: list[str] = line.split("->")
        input_module: str = splits[0].replace(" ", "")
        destination_modules: list[str] = (
            splits[1].rstrip("\n").replace(" ", "").split(",")
        )

        # Curent Module
        new_module: Module
        if input_module == "broadcaster":
            new_module = Broadcaster(input_module, [])
        elif input_module.startswith("%"):
            new_module = FlipFlop(input_module.lstrip("%"), [])
        elif input_module.startswith("&"):
            new_module = Conjunction(input_module.lstrip("&"), [])
        else:
            raise Exception("Cannot convert into a module: ", input_module)

        # Destination Modules
        modules[new_module] = destination_modules

    # Poplulate destination modules
    for key, value in modules.items():
        for module_str in value:
            m = next((m for m in modules.keys() if m.name == module_str), None)
            if m is not None:
                key.destination_modules.append(m)
            else:
                key.destination_modules.append(Module(module_str, []))

    # Populate Conjuction Modules
    for module in [m for m in modules.keys() if type(m) == Conjunction]:
        for mod in modules.keys():
            if module in mod.destination_modules:
                module.last_pulse_from_desitnations[mod] = Pulse.low

    return list(modules.keys())


def press_button(broadcaster_module: Module) -> None:
    global low_pulses_sent

    low_pulses_sent += 1
    broadcaster_module.input(Pulse.low, Module("", []))

    m: Tuple["Module", "Pulse", "Module"] | None = ModuleQueue.take()
    while m is not None:
        m[0].input(m[1], m[2])
        m = ModuleQueue.take()


if __name__ == "__main__":
    mods = get_modules_from_input()
    broadcaster_module = next(module for module in mods if module.name == "broadcaster")

    while True:
        num_butt_pressed += 1
        press_button(broadcaster_module)
        print(num_butt_pressed)

    print("High pulses sent: ", high_pulses_sent)
    print("Low pulses sent: ", low_pulses_sent)
