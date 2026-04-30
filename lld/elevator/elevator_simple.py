from enum import Enum, auto

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    IDLE = auto()

class ElevatorState(Enum):
    MOVING = auto()
    STOPPED = auto()

class Elevator:
    def __init__(self, id, current_floor=0):
        self.id = id
        self.current_floor = current_floor
        self.state = ElevatorState.STOPPED
        self.direction = Direction.IDLE
        self.targets = []  # floors to stop at (simple list instead of 2 heaps)

    def add_target(self, floor: int):
        if floor not in self.targets:
            self.targets.append(floor)

        # Decide movement direction
        if self.targets:
            if floor > self.current_floor:
                self.direction = Direction.UP
            elif floor < self.current_floor:
                self.direction = Direction.DOWN

    def step(self):
        """Move one floor per tick."""
        if not self.targets:
            self.direction = Direction.IDLE
            self.state = ElevatorState.STOPPED
            return

        target = self.targets[0]

        if self.current_floor == target:
            # Arrived
            print(f"Elevator {self.id} opening doors at floor {target}")
            self.targets.pop(0)
            if not self.targets:
                self.direction = Direction.IDLE
            self.state = ElevatorState.STOPPED
        else:
            self.state = ElevatorState.MOVING
            if target > self.current_floor:
                self.current_floor += 1
                self.direction = Direction.UP
            else:
                self.current_floor -= 1
                self.direction = Direction.DOWN

class ElevatorController:
    def __init__(self, num_elevators=2, max_floor=10):
        self.elevators = [Elevator(i) for i in range(num_elevators)]
        self.max_floor = max_floor

    def request_elevator(self, floor: int):
        # Nearest idle elevator OR elevator already moving toward that direction
        best = None
        best_distance = float('inf')

        for elevator in self.elevators:
            # Choose idle first, then closest moving towards direction
            if elevator.direction == Direction.IDLE or \
               (elevator.direction == Direction.UP and floor >= elevator.current_floor) or \
               (elevator.direction == Direction.DOWN and floor <= elevator.current_floor):

                dist = abs(elevator.current_floor - floor)
                if dist < best_distance:
                    best_distance = dist
                    best = elevator

        # Assign and return id
        best.add_target(floor)
        return best.id

    def step(self):
        for e in self.elevators:
            e.step()

    def status(self):
        for e in self.elevators:
            print(
                f"Elevator {e.id}: floor={e.current_floor}, "
                f"dir={e.direction.name}, targets={e.targets}"
            )

# ---- Simulation example ----
if __name__ == "__main__":
    controller = ElevatorController(num_elevators=2)

    controller.request_elevator(5)
    controller.request_elevator(2)

    for _ in range(10):
        controller.status()
        controller.step()
        print("---")