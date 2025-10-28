from abc import ABC, abstractmethod


# State Pattern: Abstract State
class VendingMachineState(ABC):
    """Abstract state class for vending machine states."""

    def __init__(self):
        """Initialize state with machine reference."""
        # Will be set when state is assigned to machine in change_state()
        self.machine = None

    @abstractmethod
    def select_code(self, code: str) -> None:
        """Handle code selection in current state."""
        pass

    @abstractmethod
    def insert_money(self, amount: float) -> None:
        """Handle money insertion in current state."""
        pass

    @abstractmethod
    def cancel_transaction(self) -> None:
        """Handle transaction cancellation in current state."""
        pass

    @abstractmethod
    def get_state_name(self) -> str:
        """Return the name of the current state."""
        pass


# Concrete States
class IdleState(VendingMachineState):
    """Initial state - waiting for code selection."""

    def select_code(self, code: str) -> None:
        """Select a product code."""
        if code not in self.machine.products:
            print(f"Invalid code: {code}")
            return

        product = self.machine.products[code]

        # Check if out of stock
        if product['quantity'] == 0:
            print(f"Code {code} is out of stock. Please select another code.")
            return

        # Check current payment
        if self.machine.current_payment >= product['price']:
            # Enough money, move to dispensing state
            self.machine.selected_code = code
            self.machine.change_state(DispensingState())
            self.machine.state.dispense_product()
        else:
            # Need more money, move to waiting state
            self.machine.selected_code = code
            needed = product['price'] - self.machine.current_payment
            print(
                f"Code {code} selected: {product['name']} - ${product['price']:.2f}")
            if self.machine.current_payment > 0:
                print(f"Current payment: ${self.machine.current_payment:.2f}")
                print(f"Please insert ${needed:.2f} more.")
            else:
                print(f"Please insert ${product['price']:.2f}.")
            self.machine.change_state(WaitingForPaymentState())

    def insert_money(self, amount: float) -> None:
        """No code selected yet."""
        print("Please select a code first.")

    def cancel_transaction(self) -> None:
        """Nothing to cancel."""
        print("No transaction to cancel.")

    def get_state_name(self) -> str:
        return "Idle"


class WaitingForPaymentState(VendingMachineState):
    """Waiting for user to insert sufficient payment."""

    def select_code(self, code: str) -> None:
        """Cannot select new code while waiting for payment."""
        print("Please complete current transaction first.")

    def insert_money(self, amount: float) -> None:
        """Insert money and check if sufficient."""
        if amount <= 0:
            print("Invalid amount. Please insert a positive amount.")
            return

        self.machine.current_payment += amount
        print(
            f"Inserted ${amount:.2f}. Total: ${self.machine.current_payment:.2f}")

        # Check if we have enough money now
        product = self.machine.products[self.machine.selected_code]

        if self.machine.current_payment >= product['price']:
            # Move to dispensing state
            self.machine.change_state(DispensingState())
            self.machine.state.dispense_product()
        else:
            needed = product['price'] - self.machine.current_payment
            print(f"Please insert ${needed:.2f} more.")

    def cancel_transaction(self) -> None:
        """Cancel and return money."""
        if self.machine.current_payment > 0:
            print(
                f"Transaction cancelled. Returning ${self.machine.current_payment:.2f}")
            self.machine.current_payment = 0
            self.machine.selected_code = None
            self.machine.change_state(IdleState())
        else:
            print("No transaction to cancel.")

    def get_state_name(self) -> str:
        return "Waiting for Payment"


class DispensingState(VendingMachineState):
    """Dispensing the product."""

    def select_code(self, code: str) -> None:
        """Cannot select code while dispensing."""
        print("Please wait while product is being dispensed...")

    def insert_money(self, amount: float) -> None:
        """Cannot insert money while dispensing."""
        print("Please wait while product is being dispensed...")

    def cancel_transaction(self) -> None:
        """Cannot cancel while dispensing."""
        print("Cannot cancel while dispensing product.")

    def get_state_name(self) -> str:
        return "Dispensing"

    def dispense_product(self) -> None:
        """Dispense the product and return to idle."""
        code = self.machine.selected_code
        product = self.machine.products[code]

        # Deduct inventory
        product['quantity'] -= 1

        # Calculate and return change
        change = self.machine.current_payment - product['price']

        print(f"\nDispensing {product['name']}...")
        print(f"Enjoy your {product['name']}!")

        if change > 0:
            print(f"Returning change: ${change:.2f}")

        # Reset payment and selected code
        self.machine.current_payment = 0
        self.machine.selected_code = None

        # Return to idle state
        self.machine.change_state(IdleState())


# Vending Machine
class VendingMachine:
    """
    A naive vending machine implementation using State Pattern and code-based selection.
    """

    def __init__(self):
        # Products: {code: {'name': str, 'price': float, 'quantity': int}}
        self.products = {
            'A1': {'name': 'Coke', 'price': 1.50, 'quantity': 10},
            'A2': {'name': 'Pepsi', 'price': 1.50, 'quantity': 10},
            'A3': {'name': 'Sprite', 'price': 1.50, 'quantity': 8},
            'B1': {'name': 'Water', 'price': 1.00, 'quantity': 15},
            'B2': {'name': 'Chips', 'price': 2.00, 'quantity': 5},
            'B3': {'name': 'Candy', 'price': 1.25, 'quantity': 12}
        }

        # Current state
        self.state = IdleState()
        self.state.machine = self

        # Current payment and selected code
        self.current_payment = 0.0
        self.selected_code = None

    def change_state(self, new_state: VendingMachineState) -> None:
        """Change the current state."""
        self.state = new_state
        self.state.machine = self

    def select_code(self, code: str) -> None:
        """Select a product by code."""
        self.state.select_code(code)

    def insert_money(self, amount: float) -> None:
        """Insert money into the machine."""
        self.state.insert_money(amount)

    def cancel_transaction(self) -> None:
        """Cancel the current transaction."""
        self.state.cancel_transaction()

    def display_products(self) -> None:
        """Display all available products with codes."""
        print("\n=== Vending Machine ===")
        print(f"{'Code':<8} {'Product':<15} {'Price':<10} {'In Stock':<10}")
        print("-" * 45)
        for code, info in self.products.items():
            status = f"{info['quantity']}" if info['quantity'] > 0 else "Sold Out"
            print(
                f"{code:<8} {info['name']:<15} ${info['price']:<9.2f} {status}")
        print()

    def get_state_name(self) -> str:
        """Get the current state name."""
        return self.state.get_state_name()


def main():
    """Demo of the vending machine with State Pattern."""
    vm = VendingMachine()

    print("Welcome to the Vending Machine!")
    vm.display_products()

    # Demo: Select code and insert money
    print("\n--- Example 1: Select A1 (Coke) ---")
    vm.insert_money(2.00)  # Will prompt to select code first
    vm.select_code("A1")
    vm.insert_money(1.50)  # Complete the purchase

    print("\n--- Example 2: Select B3 (Candy) with insufficient funds ---")
    vm.select_code("B3")  # Needs $1.25
    vm.insert_money(1.00)  # Still short by $0.25
    vm.insert_money(0.50)  # Now have $1.50, enough to purchase

    print("\n--- Example 3: Select B2 (Chips) ---")
    vm.select_code("B2")  # Needs $2.00
    vm.insert_money(1.00)  # Not enough
    vm.insert_money(1.50)  # Total $2.50, enough to purchase

    print("\n--- Example 4: Cancel transaction ---")
    vm.insert_money(5.00)
    vm.select_code("A2")  # Select product
    vm.cancel_transaction()

    print("\n--- Example 5: Final inventory ---")
    vm.display_products()


if __name__ == "__main__":
    main()
