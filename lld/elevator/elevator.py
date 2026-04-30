from abc import ABC, abstractmethod
from enum import Enum
import heapq


class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    IDLE = 'idle'


class Request:
    def __init__(self, floor, direction):
        self.floor = floor
        self.direction = direction

    def __lt__(self, other):
        """Required for heapq to work correctly."""
        # For UP queue: lower floors have priority
        # For DOWN queue: higher floors have priority
        return self.floor < other.floor

    def __repr__(self):
        return f"Request(floor={self.floor}, dir={self.direction.value})"


class Elevator:
    def __init__(self, floor_number):
        self.state = IdleState()
        self.state.set_context(self)
        self.current_floor_number = 0
        self.queue_up = []  # Min heap for floors going up
        self.queue_down = []  # Min heap for floors going down
        self.direction = Direction.IDLE
        self.max_floor_number = floor_number
        # Track which floors are requested for quick lookup
        self.requested_floors_up = set()
        self.requested_floors_down = set()

    def set_state(self, state):
        self.state = state
        self.state.set_context(self)

    def request_floor(self, request):
        self.state.request_floor(request)

    def move(self):
        """Move elevator one floor. Called repeatedly when moving."""
        self.state.move()

    def check_and_stop_at_current_floor(self):
        """Check if current floor is in request queues and stop if needed."""
        current = self.current_floor_number

        if self.direction == Direction.UP:
            # Check if current floor is requested going up
            if current in self.requested_floors_up:
                # Remove from queue and set
                self.remove_floor_from_up_queue(current)
                self.set_state(DoorOpenState())
                return True
        elif self.direction == Direction.DOWN:
            # Check if current floor is requested going down
            if current in self.requested_floors_down:
                self.remove_floor_from_down_queue(current)
                self.set_state(DoorOpenState())
                return True
        return False

    def remove_floor_from_up_queue(self, floor):
        """Remove a specific floor from UP queue."""
        if floor in self.requested_floors_up:
            self.requested_floors_up.remove(floor)
            # Rebuild heap without this floor
            self.queue_up = [r for r in self.queue_up if r.floor != floor]
            heapq.heapify(self.queue_up)

    def remove_floor_from_down_queue(self, floor):
        """Remove a specific floor from DOWN queue."""
        if floor in self.requested_floors_down:
            self.requested_floors_down.remove(floor)
            # Rebuild heap without this floor
            self.queue_down = [r for r in self.queue_down if r.floor != floor]
            heapq.heapify(self.queue_down)

    def has_more_requests_in_direction(self):
        """Check if there are more requests in current direction."""
        if self.direction == Direction.UP:
            return len(self.queue_up) > 0
        elif self.direction == Direction.DOWN:
            return len(self.queue_down) > 0
        return False


class ElevatorState(ABC):
    def __init__(self):
        self._context = None

    def set_context(self, context):
        self._context = context

    @abstractmethod
    def request_floor(self, request):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def get_state_name(self):
        pass


class IdleState(ElevatorState):
    def request_floor(self, request):
        """Add request and determine direction."""
        if request.floor == self._context.current_floor_number:
            print(f"Already on floor {request.floor}")
            return

        if request.floor > self._context.current_floor_number:
            heapq.heappush(self._context.queue_up, request)
            self._context.requested_floors_up.add(request.floor)
            self._context.direction = Direction.UP
            print(
                f"Added request for floor {request.floor} (UP). Current floor: {self._context.current_floor_number}")
        else:
            heapq.heappush(self._context.queue_down, request)
            self._context.requested_floors_down.add(request.floor)
            self._context.direction = Direction.DOWN
            print(
                f"Added request for floor {request.floor} (DOWN). Current floor: {self._context.current_floor_number}")

        # Start moving
        self._context.set_state(MovingState())

    def move(self):
        """Nothing to do when idle."""
        pass

    def get_state_name(self):
        return "Idle"


class MovingState(ElevatorState):
    def request_floor(self, request):
        """Add request to appropriate queue while moving."""
        if request.floor == self._context.current_floor_number:
            print(f"Already at floor {request.floor}")
            return

        current = self._context.current_floor_number
        current_dir = self._context.direction

        # Add to queue based on floor position, not request direction
        if request.floor > current:
            heapq.heappush(self._context.queue_up, request)
            self._context.requested_floors_up.add(request.floor)
            print(
                f"Added floor {request.floor} to UP queue (currently at {current})")
        else:
            heapq.heappush(self._context.queue_down, request)
            self._context.requested_floors_down.add(request.floor)
            print(
                f"Added floor {request.floor} to DOWN queue (currently at {current})")

    def move(self):
        """Move one floor in current direction."""
        if self._context.direction == Direction.UP:
            if self._context.current_floor_number >= self._context.max_floor_number:
                # Can't go higher, switch direction or idle
                if len(self._context.queue_down) > 0:
                    self._context.direction = Direction.DOWN
                    print(f"Reached top floor. Switching to DOWN direction.")
                else:
                    self._context.direction = Direction.IDLE
                    self._context.set_state(IdleState())
                return

            # Move up one floor
            self._context.current_floor_number += 1
            print(f"Moving UP to floor {self._context.current_floor_number}")

        elif self._context.direction == Direction.DOWN:
            if self._context.current_floor_number <= 0:
                # Can't go lower, switch direction or idle
                if len(self._context.queue_up) > 0:
                    self._context.direction = Direction.UP
                    print(f"Reached bottom floor. Switching to UP direction.")
                else:
                    self._context.direction = Direction.IDLE
                    self._context.set_state(IdleState())
                return

            # Move down one floor
            self._context.current_floor_number -= 1
            print(f"Moving DOWN to floor {self._context.current_floor_number}")

        # Check if should stop at this floor
        if self._context.check_and_stop_at_current_floor():
            print(f"Stopped at floor {self._context.current_floor_number}")
            return

        # If no requests in current direction, check opposite direction
        if not self._context.has_more_requests_in_direction():
            if self._context.direction == Direction.UP and len(self._context.queue_down) > 0:
                self._context.direction = Direction.DOWN
                print("No more UP requests. Switching to DOWN direction.")
            elif self._context.direction == Direction.DOWN and len(self._context.queue_up) > 0:
                self._context.direction = Direction.UP
                print("No more DOWN requests. Switching to UP direction.")
            elif len(self._context.queue_up) == 0 and len(self._context.queue_down) == 0:
                self._context.direction = Direction.IDLE
                self._context.set_state(IdleState())
                print("No more requests. Returning to IDLE.")

    def get_state_name(self):
        return f"Moving {self._context.direction.value}"


class DoorOpenState(ElevatorState):
    def request_floor(self, request):
        """Accept requests while door is open."""
        print(
            f"Request for floor {request.floor} received while door is open.")
        if request.floor == self._context.current_floor_number:
            print(f"Already at floor {request.floor}")
            return

        # Add to appropriate queue
        if request.floor > self._context.current_floor_number:
            heapq.heappush(self._context.queue_up, request)
            self._context.requested_floors_up.add(request.floor)
        else:
            heapq.heappush(self._context.queue_down, request)
            self._context.requested_floors_down.add(request.floor)

    def move(self):
        """Cannot move while door is open. Close door first."""
        print(
            f"Door open at floor {self._context.current_floor_number}. Closing door...")
        self._context.set_state(DoorClosedState())

    def get_state_name(self):
        return "Door Open"


class DoorClosedState(ElevatorState):
    def request_floor(self, request):
        """Accept requests and add to queue."""
        if request.floor == self._context.current_floor_number:
            print(f"Already at floor {request.floor}")
            return

        if request.floor > self._context.current_floor_number:
            heapq.heappush(self._context.queue_up, request)
            self._context.requested_floors_up.add(request.floor)
        else:
            heapq.heappush(self._context.queue_down, request)
            self._context.requested_floors_down.add(request.floor)

    def move(self):
        """After closing door, decide next state."""
        # Determine direction if idle
        if self._context.direction == Direction.IDLE:
            if len(self._context.queue_up) > 0:
                self._context.direction = Direction.UP
            elif len(self._context.queue_down) > 0:
                self._context.direction = Direction.DOWN

        # Check if should continue moving
        if self._context.has_more_requests_in_direction():
            self._context.set_state(MovingState())
            print(
                f"Door closed. Continuing in {self._context.direction.value} direction.")
        else:
            # Check opposite direction
            if self._context.direction == Direction.UP and len(self._context.queue_down) > 0:
                self._context.direction = Direction.DOWN
                self._context.set_state(MovingState())
                print("Switching to DOWN direction.")
            elif self._context.direction == Direction.DOWN and len(self._context.queue_up) > 0:
                self._context.direction = Direction.UP
                self._context.set_state(MovingState())
                print("Switching to UP direction.")
            else:
                # No more requests
                self._context.direction = Direction.IDLE
                self._context.set_state(IdleState())
                print("No more requests. Returning to IDLE.")

    def get_state_name(self):
        return "Door Closed"


# Demo/test code
if __name__ == "__main__":
    print("=== Elevator System Demo ===\n")

    elevator = Elevator(10)

    # Add some requests
    print("Adding requests:")
    elevator.request_floor(Request(5, Direction.UP))
    elevator.request_floor(Request(3, Direction.DOWN))
    elevator.request_floor(Request(7, Direction.UP))

    print("\n=== Starting elevator movement ===\n")

    # Simulate movement (in real system, this would be time-based)
    max_iterations = 50
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        state_name = elevator.state.get_state_name()

        if state_name == "Idle" and len(elevator.queue_up) == 0 and len(elevator.queue_down) == 0:
            print("\n=== All requests completed ===")
            break

        # Move or process state
        elevator.move()

        # If door is open, wait a bit then close
        if state_name == "Door Open":
            elevator.move()  # This will close the door

        print()  # Blank line for readability

    print(f"\nFinal floor: {elevator.current_floor_number}")
    print(f"Final state: {elevator.state.get_state_name()}")
