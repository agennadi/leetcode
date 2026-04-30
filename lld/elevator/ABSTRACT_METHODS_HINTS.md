# Abstract Methods for Elevator State Pattern - Hints

## 🎯 Key Actions an Elevator Can Perform

Think about **what actions can be triggered** in different states:

### 1. **External Request** (Floor Button Press)
- User on floor presses UP or DOWN button
- Should work differently based on current state:
  - **IDLE**: Accept request, determine direction, start moving
  - **MOVING_UP**: Add to queue if going up, queue for later if going down
  - **DOOR_OPEN**: Queue request, close door first

### 2. **Internal Request** (Elevator Button Press)
- User inside elevator presses floor number button
- Should work differently based on current state:
  - **IDLE**: Accept, start moving
  - **MOVING**: Add to queue
  - **DOOR_OPEN**: Accept, close door when ready

### 3. **Move/Step**
- Elevator moves one floor up or down
- Happens automatically when moving
- Should check if we've reached a requested floor

### 4. **Arrival at Floor**
- Elevator reaches a floor
- Should check if this floor is in the request queue
- If yes: stop, open door
- If no: continue moving

### 5. **Open Door**
- Open doors at destination floor
- Transition from MOVING → DOOR_OPEN
- Should work in STOPPED state

### 6. **Close Door**
- Close doors after passengers board/exit
- Transition from DOOR_OPEN → MOVING or IDLE
- Should work in DOOR_OPEN state

---

## 💡 Suggested Abstract Methods

```python
class ElevatorState(ABC):
    def __init__(self):
        self.elevator = None  # Reference to Elevator context
    
    @abstractmethod
    def handle_external_request(self, floor: int, direction: Direction) -> None:
        """Handle request from floor button press."""
        pass
    
    @abstractmethod
    def handle_internal_request(self, floor: int) -> None:
        """Handle request from inside elevator button press."""
        pass
    
    @abstractmethod
    def move(self) -> None:
        """Move elevator one floor (called periodically when moving)."""
        pass
    
    @abstractmethod
    def arrive_at_floor(self, floor: int) -> None:
        """Called when elevator reaches a floor. Check if should stop."""
        pass
    
    @abstractmethod
    def open_door(self) -> None:
        """Open elevator doors."""
        pass
    
    @abstractmethod
    def close_door(self) -> None:
        """Close elevator doors."""
        pass
    
    @abstractmethod
    def get_state_name(self) -> str:
        """Return state name (for debugging)."""
        pass
```

---

## 🤔 Alternative: Simplified Approach

If you want to start simpler, focus on **core actions** first:

```python
class ElevatorState(ABC):
    @abstractmethod
    def handle_request(self, floor: int, direction: Direction = None) -> None:
        """Handle both external and internal requests."""
        pass
    
    @abstractmethod
    def move(self) -> None:
        """Move one floor (called on each time step)."""
        pass
    
    @abstractmethod
    def stop(self) -> None:
        """Stop at current floor (if it's in request queue)."""
        pass
```

---

## 📋 Method Behavior by State

### **IdleState**
- `handle_external_request()`: Accept request, change to MOVING_UP or MOVING_DOWN
- `handle_internal_request()`: Accept request, start moving
- `move()`: Nothing (not moving)
- `open_door()`: Transition to DOOR_OPEN
- `close_door()`: Nothing (door already closed)

### **MovingUpState**
- `handle_external_request()`: Add to queue if floor > current, queue if floor < current
- `handle_internal_request()`: Add to upward queue
- `move()`: Increment floor by 1, check if arrived at requested floor
- `arrive_at_floor()`: If floor in queue, stop and open door
- `open_door()`: Not allowed while moving
- `close_door()`: Not applicable

### **DoorOpenState**
- `handle_external_request()`: Add to queue
- `handle_internal_request()`: Add to queue
- `move()`: Not allowed (door is open)
- `close_door()`: Close door, transition to MOVING or IDLE
- `open_door()`: Already open

---

## 🎯 My Recommendation

Start with these **essential methods**:

```python
class ElevatorState(ABC):
    def __init__(self):
        self.elevator = None
    
    @abstractmethod
    def request_floor(self, floor: int) -> None:
        """
        Handle floor request (works for both external and internal).
        Simplify by letting elevator determine if it's external/internal.
        """
        pass
    
    @abstractmethod
    def move(self) -> None:
        """
        Move elevator one floor in current direction.
        Check if reached destination, handle state transitions.
        """
        pass
    
    @abstractmethod
    def stop_at_floor(self, floor: int) -> None:
        """
        Stop elevator at floor and open door.
        Called when elevator arrives at a requested floor.
        """
        pass
    
    @abstractmethod
    def get_state_name(self) -> str:
        """Return state name."""
        pass
```

---

## 💭 Think About...

1. **What actions can happen in each state?**
   - IDLE: Can accept requests, can open door
   - MOVING: Can accept requests, can move, can stop
   - DOOR_OPEN: Can accept requests, can close door

2. **Which actions trigger state changes?**
   - Request in IDLE → MOVING
   - Arrive at floor → DOOR_OPEN
   - Close door → MOVING or IDLE

3. **What's the simplest interface?**
   - Start with 3-4 core methods
   - Add more later if needed
   - Don't over-complicate initially

---

## ✅ Checklist

- [ ] Abstract methods cover all possible actions
- [ ] Each method makes sense in context of elevator behavior
- [ ] Methods allow states to transition appropriately
- [ ] Not too many methods (aim for 3-6)
- [ ] Methods are meaningful (not just getters/setters)

**Start simple, add complexity later!** 🚀

