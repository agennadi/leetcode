# Naive Vending Machine

A vending machine implementation in Python using the **State Pattern** for managing different states of operation.

## Features

- **State Pattern**: Properly manages different states (Idle, Waiting for Payment, Dispensing)
- **Code-based selection**: Products are selected by codes (e.g., A1, B2, C3)
- Display available products with codes, prices and stock
- Insert money for purchases
- Select products by code
- Automatic change return
- Track inventory
- Handle insufficient funds
- Cancel transactions
- Proper state transitions

## Vending Machine States

1. **IdleState**: Waiting for code selection
2. **WaitingForPaymentState**: Code selected, waiting for sufficient payment
3. **DispensingState**: Dispensing the product

## Usage

Run the vending machine:
```bash
python3 vending_machine.py
```

## Code Example

```python
from vending_machine import VendingMachine

vm = VendingMachine()

# Display available products with codes
vm.display_products()

# Select a product by code
vm.select_code("A1")  # Select Coke

# Insert money
vm.insert_money(1.50)  # Enough to purchase

# Or insert money in multiple increments
vm.insert_money(1.00)  # Partial payment
vm.insert_money(0.50)  # Complete payment

# Cancel transaction (if needed)
vm.cancel_transaction()

# Check current state
print(vm.get_state_name())
```

## Product Codes

- **A1**: Coke ($1.50)
- **A2**: Pepsi ($1.50)
- **A3**: Sprite ($1.50)
- **B1**: Water ($1.00)
- **B2**: Chips ($2.00)
- **B3**: Candy ($1.25)

## API

### `display_products()`
Shows all products with codes, names, prices, and stock levels.

### `select_code(code: str)`
Select a product by its code (e.g., "A1", "B2").
- Behavior depends on current state
- In Idle state: selects product and checks payment
- In other states: prevents selection

### `insert_money(amount: float)`
Insert money into the machine.
- Behavior depends on current state
- In Idle state: prompts to select code first
- In WaitingForPaymentState: accumulates payment

### `cancel_transaction()`
Cancel the current transaction and return any inserted money.
- Returns machine to IdleState
- Behavior depends on current state

### `get_state_name()`
Returns the name of the current state.

