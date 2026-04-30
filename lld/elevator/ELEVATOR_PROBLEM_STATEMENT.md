# Elevator System - Low Level Design Problem

## Problem Statement

Design and implement an Elevator Control System that can handle multiple elevators, floor requests, and optimize elevator movement based on request patterns. The system should efficiently manage passenger requests and coordinate multiple elevators in a building.

---

## Functional Requirements

### 1. Elevator Management
- Support **multiple elevators** in a building (e.g., 2-4 elevators)
- Each elevator should track:
  - Current floor
  - Direction (UP, DOWN, IDLE)
  - Current state (MOVING, STOPPED, DOOR_OPEN, DOOR_CLOSED)
  - Floor requests (which floors to visit)

### 2. Request Handling
- **Floor requests**: Users press buttons on floors to call elevator
- **Internal requests**: Users press buttons inside elevator to select destination floor
- System should:
  - Accept requests from any floor
  - Assign requests to appropriate elevator
  - Queue multiple requests efficiently

### 3. Elevator Movement
- Elevator moves one floor at a time
- Determine direction based on pending requests
- Stop at requested floors
- Open/close doors at stops
- Handle requests in optimal order (minimize wait time)

### 4. Direction Management
- **UP direction**: Pick up requests going up, drop off passengers going up
- **DOWN direction**: Pick up requests going down, drop off passengers going down
- **IDLE**: No pending requests, elevator waits
- Elevator should continue in current direction if there are requests ahead

### 5. Button System
- **External buttons** (on floors): UP button, DOWN button
- **Internal buttons** (inside elevator): Floor number buttons (1-N)
- Button press generates a request

---

## Non-Functional Requirements

1. **Efficiency**: Minimize average waiting time
2. **Scalability**: Support buildings with different numbers of floors
3. **Thread Safety**: Handle concurrent requests (multiple users pressing buttons simultaneously)
4. **Maintainability**: Code should be extensible for future features

---

## Design Constraints

1. Use **State Pattern** for elevator states (IDLE, MOVING_UP, MOVING_DOWN, DOOR_OPEN, etc.)
2. Use **Strategy Pattern** for elevator scheduling algorithms (optional)
3. Follow SOLID principles
4. Consider thread safety for concurrent requests

---

## Edge Cases to Handle

1. Multiple requests on same floor
2. Request when elevator is already moving
3. Request in opposite direction when elevator is moving
4. Request for current floor
5. All elevators busy - queue the request
6. Elevator capacity limit reached (optional)
7. Emergency stop button pressed
8. Power failure scenario (optional)
9. Multiple elevators - which one to assign?
10. User presses button while door is opening/closing

---

## Elevator States

- **IDLE**: Elevator is stationary, no requests
- **MOVING_UP**: Elevator moving up, has requests in upward direction
- **MOVING_DOWN**: Elevator moving down, has requests in downward direction
- **DOOR_OPENING**: Doors are opening
- **DOOR_OPEN**: Doors are open, passengers can enter/exit
- **DOOR_CLOSING**: Doors are closing
- **STOPPED**: Temporarily stopped (between MOVING states)

---

## Example Scenarios

### Scenario 1: Simple Request
```
1. User on Floor 3 presses UP button
2. Elevator (currently at Floor 1) receives request
3. Elevator moves to Floor 3 (state: MOVING_UP)
4. Elevator stops at Floor 3 (state: STOPPED)
5. Door opens (state: DOOR_OPEN)
6. User enters, presses Floor 5
7. Door closes, elevator moves to Floor 5
8. Door opens, user exits
9. Elevator returns to IDLE
```

### Scenario 2: Multiple Requests
```
1. Floor 2: UP request
2. Floor 5: DOWN request
3. Inside Elevator: User wants Floor 8
4. Elevator at Floor 1:
   - Goes to Floor 2 (pick up)
   - Goes to Floor 5 (pick up going down)
   - Goes to Floor 8 (drop off)
   - Goes back to Floor 5 (drop off)
```

### Scenario 3: Opposite Direction Request
```
1. Elevator moving UP to Floor 5
2. Floor 2 gets DOWN request (while elevator moving up)
3. Elevator completes UP journey first
4. Then changes direction to DOWN to serve Floor 2
```

---

## Elevator Scheduling Strategy (Simplified)

**Simple Strategy:**
- If elevator is IDLE: Move to requested floor
- If elevator is MOVING_UP: 
  - Add request if floor is above current floor
  - Queue request if floor is below (handle after completing UP journey)
- If elevator is MOVING_DOWN:
  - Add request if floor is below current floor
  - Queue request if floor is above (handle after completing DOWN journey)

---

## Expected Deliverables

1. **Core Classes**:
   - `Elevator` - Represents an elevator with state management
   - `Building` - Manages multiple elevators
   - `Floor` - Represents a floor with buttons
   - `Request` - Represents a floor request
   - `Button` - Represents elevator/floor buttons

2. **State Classes** (State Pattern):
   - `ElevatorState` (abstract)
   - `IdleState`, `MovingUpState`, `MovingDownState`, `DoorOpenState`, etc.

3. **Implementation** with:
   - Request queuing system
   - State transitions
   - Movement logic
   - Button handling

4. **Test Cases** for various scenarios

---

## Bonus Features (Optional)

1. **Multiple Elevator Coordination**:
   - Assign request to nearest available elevator
   - Load balancing across elevators

2. **Priority System**:
   - VIP mode (skip floors)
   - Emergency priority

3. **Smart Scheduling**:
   - Predict optimal path
   - Minimize total travel time

4. **Capacity Management**:
   - Track number of passengers
   - Skip floors if at capacity

5. **Maintenance Mode**:
   - Take elevator out of service
   - Display maintenance status

---

## Questions to Consider

1. How should the system handle requests when all elevators are busy?
2. Should elevators continue in same direction if more requests come?
3. How to decide which elevator serves a request when multiple are available?
4. What happens if user presses button multiple times?
5. Should elevator wait for more requests if door is open?
6. How to handle simultaneous UP and DOWN requests on same floor?

---

## Success Criteria

Your implementation is successful if it:
- ✅ Handles floor requests correctly
- ✅ Manages elevator states and transitions
- ✅ Processes requests in logical order
- ✅ Handles multiple elevators (if implemented)
- ✅ Code is clean, maintainable, follows OOP principles
- ✅ Uses appropriate design patterns (State Pattern required)

---

**Note**: Start simple - implement single elevator first, then extend to multiple elevators.

Good luck! 🏢

