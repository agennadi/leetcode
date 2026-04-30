# Vending Machine Design Explanation

## Your Questions Answered

### Question 1: Why doesn't the abstract state class have the "machine" attribute? Doesn't it go against the Liskov Principle?

**Answer:** You were absolutely right! This was a design flaw.

**Original Problem:**
- The abstract class `VendingMachineState` didn't define the `machine` attribute
- Each concrete state had a `machine` attribute
- This violates the **Liskov Substitution Principle** because the abstract class wasn't defining the full interface that all subclasses need

**The Fix:**
```python
class VendingMachineState(ABC):
    def __init__(self):
        """Initialize state with machine reference."""
        # Will be set when state is assigned to machine in change_state()
        self.machine = None
```

Now:
- The abstract class defines the `machine` attribute that all states need
- All states inherit this attribute, making the interface consistent
- We can safely assume any state object has a `machine` attribute
- This follows the **Liskov Substitution Principle** - any state can be used where the abstract type is expected

---

### Question 2: Why do we assign machine in two places?

**Original Problem:**
1. In `change_state()`: `self.state.machine = self`
2. In each state method: `machine = self._get_machine()` which returned `self.machine`

This was **redundant** and confusing!

**Why we needed both (before the fix):**
- The first assignment (`self.state.machine = self`) sets up the bidirectional relationship
- The second retrieval (`machine = self._get_machine()`) was supposed to make the code "cleaner" 
- But it was actually **pointless** - we were just retrieving what we already set

**The Fix:**
Now we only do it once in `change_state()`:
```python
def change_state(self, new_state: VendingMachineState) -> None:
    """Change the current state."""
    self.state = new_state
    self.state.machine = self  # Set the machine reference once
```

And we use it directly in states:
```python
def select_code(self, code: str) -> None:
    """Select a product code."""
    if code not in self.machine.products:  # Use self.machine directly
        print(f"Invalid code: {code}")
        return
```

**No more redundant `_get_machine()` helper needed!**

---

## State Pattern Flow

1. **State Creation**: When a new state is created (`IdleState()`, `WaitingForPaymentState()`, etc.), the `__init__()` from the abstract class sets `self.machine = None`

2. **State Assignment**: When `change_state()` is called, it assigns `self.state.machine = self`, establishing the bidirectional relationship

3. **State Usage**: Each state method uses `self.machine` directly to access the vending machine's data and methods

## Benefits of This Design

1. **Single Source of Truth**: The machine reference is set once in `change_state()`
2. **No Redundancy**: We don't need helper methods like `_get_machine()`
3. **Clean Interface**: The abstract class defines what all states need
4. **Liskov Compliant**: All states can be used interchangeably
5. **Clear Ownership**: The relationship between machine and state is explicit

