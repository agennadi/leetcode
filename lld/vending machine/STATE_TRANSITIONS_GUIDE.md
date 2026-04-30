# State Pattern Guide - Understanding State Transitions

## Key Concepts

### 1. **States DON'T Change Themselves**
❌ **WRONG:**
```python
class OutOfStockState(State):
    def handle_input(self, input):
        self.context.state = TransactionCancelledState()  # State changing itself!
```

✅ **CORRECT:**
```python
class OutOfStockState(State):
    def handle_input(self, input):
        self.machine.change_state(TransactionCancelledState())  # Context changes state
```

### 2. **Context (VendingMachine) Controls State Changes**
The `VendingMachine` class has a `change_state()` method. This is the **ONLY** place states should change.

```python
class VendingMachine:
    def change_state(self, new_state: VendingMachineState) -> None:
        """This is the ONLY way states should change."""
        self.state = new_state
        self.state.set_machine(self)  # Give new state reference to machine
```

### 3. **Each State Handles Specific Actions**
Instead of a generic `handle_input()`, each state implements specific methods:
- `select_code(code)`
- `insert_money(amount)`
- `cancel_transaction()`

## State Flow Diagram

```
┌─────────────┐
│ IdleState   │  ←──────────┐
└─────────────┘            │
      │                    │
      │ select_code()      │
      ▼                    │
┌─────────────────────┐    │
│ WaitingForPayment   │    │
│ State              │    │
└─────────────────────┘    │
      │                    │
      │ insert_money()     │
      │ (enough $)         │
      ▼                    │
┌─────────────┐            │
│ Dispensing  │            │
│ State       │────────────┘
└─────────────┘
```

## State Transition Rules

### **IdleState** → WaitingForPaymentState
- When: User selects valid code that's in stock
- Trigger: `select_code()` finds valid product
- Action: Store selected product, check payment

### **IdleState** → DispensingState
- When: User selects code AND already has enough money
- Trigger: `select_code()` finds product AND `current_payment >= product.price`
- Action: Skip payment step, go straight to dispensing

### **WaitingForPaymentState** → DispensingState
- When: User inserts enough money
- Trigger: `insert_money()` makes `current_payment >= product.price`
- Action: Start dispensing

### **WaitingForPaymentState** → IdleState
- When: User cancels transaction
- Trigger: `cancel_transaction()`
- Action: Return money, clear selection

### **DispensingState** → IdleState
- When: Product dispensed successfully
- Trigger: `dispense_product()` completes
- Action: Reset payment, clear selection, update inventory

## Code Structure

```python
# 1. Abstract State (defines interface)
class VendingMachineState(ABC):
    def __init__(self):
        self.machine = None  # Reference to context
    
    @abstractmethod
    def select_code(self, code): pass
    @abstractmethod
    def insert_money(self, amount): pass
    @abstractmethod
    def cancel_transaction(self): pass

# 2. Concrete States (implement behavior)
class IdleState(VendingMachineState):
    def select_code(self, code):
        # Check product, then:
        self.machine.change_state(WaitingForPaymentState())  # ✅ Context changes state
    
    def insert_money(self, amount):
        print("Select code first")  # Invalid in this state

# 3. Context (manages state changes)
class VendingMachine:
    def __init__(self):
        self.state = IdleState()
        self.state.set_machine(self)  # Give state reference to context
    
    def change_state(self, new_state):
        self.state = new_state
        self.state.set_machine(self)  # ✅ ONLY place states change
    
    def select_code(self, code):
        self.state.select_code(code)  # Delegate to current state
```

## Common Mistakes to Avoid

### ❌ Mistake 1: State changing itself
```python
class WaitingForPaymentState:
    def insert_money(self, amount):
        self.machine.state = DispensingState()  # ❌ WRONG
```
**Fix:** Use `self.machine.change_state(DispensingState())`

### ❌ Mistake 2: Generic handle_input
```python
def handle_input(self, input):
    if input == "code":
        # ...
    elif input == "money":
        # ...
```
**Fix:** Use specific methods: `select_code()`, `insert_money()`, etc.

### ❌ Mistake 3: States don't know about machine
```python
class IdleState:
    def select_code(self, code):
        # How do I access inventory? ❌
```
**Fix:** Store `self.machine` reference, use `self.machine.inventory`

### ❌ Mistake 4: Changing state in wrong place
```python
class VendingMachine:
    def select_code(self, code):
        self.state = WaitingForPaymentState()  # ❌ Should use change_state()
```
**Fix:** Always use `self.change_state()`

## Testing State Transitions

To verify your states work correctly, test each transition:

```python
vm = VendingMachine(inventory)

# Test: Idle -> WaitingForPayment
print(vm.get_state_name())  # Should be "Idle"
vm.select_code("A1")
print(vm.get_state_name())  # Should be "Waiting for Payment"

# Test: WaitingForPayment -> Dispensing
vm.insert_money(1.50)
print(vm.get_state_name())  # Should be "Dispensing" then "Idle"

# Test: WaitingForPayment -> Idle (cancel)
vm.select_code("A2")
vm.cancel_transaction()
print(vm.get_state_name())  # Should be "Idle"
```

## Summary

1. **States delegate to context** - States call `self.machine.change_state()` to change states
2. **Context owns state changes** - `VendingMachine.change_state()` is the only place states change
3. **States access context** - States use `self.machine` to access inventory, payment, etc.
4. **Each action is explicit** - `select_code()`, `insert_money()`, `cancel_transaction()` instead of generic `handle_input()`

Follow this pattern and your state management will be clean and maintainable! 🎯

