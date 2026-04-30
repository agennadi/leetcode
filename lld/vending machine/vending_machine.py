from abc import ABC, abstractmethod
from typing import Optional


class Product:
    """Represents a product in the vending machine."""

    def __init__(self, code: str, name: str, price: float, quantity: int):
        self.code = code
        self.name = name
        self.price = price
        self.quantity = quantity


class Inventory:
    """Manages product inventory."""

    def __init__(self, products: Optional[list] = None):
        self.products = products or []
        # Create a dict for quick lookup: {code: product}
        self.product_map = {product.code: product for product in self.products}

    def get_product(self, code: str) -> Optional[Product]:
        """Get product by code."""
        return self.product_map.get(code)

    def is_in_stock(self, code: str) -> bool:
        """Check if product is in stock."""
        product = self.get_product(code)
        return product is not None and product.quantity > 0

    def reduce_quantity(self, code: str, amount: int = 1) -> bool:
        """Reduce product quantity. Returns True if successful."""
        product = self.get_product(code)
        if product and product.quantity >= amount:
            product.quantity -= amount
            return True
        return False


# ============= STATE PATTERN =============

class VendingMachineState(ABC):
    """Abstract state class. All states must implement these actions."""

    def __init__(self):
        """Initialize state. Machine reference will be set by context."""
        self.machine = None

    def set_machine(self, machine):
        """Set the machine context (called by VendingMachine)."""
        self.machine = machine

    @abstractmethod
    def select_code(self, code: str) -> None:
        """Handle product code selection."""
        pass

    @abstractmethod
    def insert_money(self, amount: float) -> None:
        """Handle money insertion."""
        pass

    @abstractmethod
    def cancel_transaction(self) -> None:
        """Handle transaction cancellation."""
        pass

    @abstractmethod
    def get_state_name(self) -> str:
        """Return state name for debugging."""
        pass


class IdleState(VendingMachineState):
    """
    Initial state - waiting for user to select a product code.

    Transitions:
    - select_code() -> WaitingForPaymentState (if in stock)
    - select_code() -> stays in IdleState (if invalid/out of stock)
    """

    def select_code(self, code: str) -> None:
        """Select a product code."""
        product = self.machine.inventory.get_product(code)

        # Check if product exists
        if product is None:
            print(f"Invalid code: {code}")
            return

        # Check if product is in stock
        if not self.machine.inventory.is_in_stock(code):
            print(f"Code {code} ({product.name}) is out of stock.")
            return

        # Valid product selected
        self.machine.selected_product = product
        print(f"Selected: {product.name} - ${product.price:.2f}")

        # Check if user already has enough money inserted
        if self.machine.current_payment >= product.price:
            # Enough money! Go directly to dispensing
            self.machine.change_state(DispensingState())
            self.machine.state.dispense_product()
        else:
            # Need more money - transition to waiting for payment
            needed = product.price - self.machine.current_payment
            if self.machine.current_payment > 0:
                print(
                    f"Current payment: ${self.machine.current_payment:.2f}. Need ${needed:.2f} more.")
            else:
                print(f"Please insert ${product.price:.2f}.")
            self.machine.change_state(WaitingForPaymentState())

    def insert_money(self, amount: float) -> None:
        """Cannot insert money before selecting a product."""
        print("Please select a product code first.")

    def cancel_transaction(self) -> None:
        """Nothing to cancel in idle state."""
        print("No transaction to cancel.")

    def get_state_name(self) -> str:
        return "Idle"


class WaitingForPaymentState(VendingMachineState):
    """
    Waiting for user to insert sufficient payment.

    Transitions:
    - insert_money() -> DispensingState (if enough money)
    - insert_money() -> stays in WaitingForPaymentState (if not enough)
    - cancel_transaction() -> IdleState
    """

    def select_code(self, code: str) -> None:
        """Cannot select another code while payment is in progress."""
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
        product = self.machine.selected_product
        if product is None:
            # This shouldn't happen, but handle it gracefully
            print("Error: No product selected.")
            self.machine.change_state(IdleState())
            return

        if self.machine.current_payment >= product.price:
            # Enough money! Move to dispensing
            self.machine.change_state(DispensingState())
            self.machine.state.dispense_product()
        else:
            # Still need more money
            needed = product.price - self.machine.current_payment
            print(f"Please insert ${needed:.2f} more.")

    def cancel_transaction(self) -> None:
        """Cancel transaction and return money."""
        if self.machine.current_payment > 0:
            print(
                f"Transaction cancelled. Returning ${self.machine.current_payment:.2f}")
            self.machine.current_payment = 0
            self.machine.selected_product = None
            self.machine.change_state(IdleState())
        else:
            print("No transaction to cancel.")
            self.machine.change_state(IdleState())

    def get_state_name(self) -> str:
        return "Waiting for Payment"


class DispensingState(VendingMachineState):
    """
    Dispensing the product.

    Transitions:
    - After dispensing -> IdleState
    """

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
        """Dispense product and return to idle."""
        product = self.machine.selected_product

        if product is None:
            print("Error: No product to dispense.")
            self.machine.change_state(IdleState())
            return

        # Reduce inventory
        if not self.machine.inventory.reduce_quantity(product.code, 1):
            print(f"Error: Could not dispense {product.name}")
            self.machine.change_state(IdleState())
            return

        # Calculate change
        change = self.machine.current_payment - product.price

        # Dispense product
        print(f"\nDispensing {product.name}...")
        print(f"Enjoy your {product.name}!")

        # Return change if any
        if change > 0:
            print(f"Returning change: ${change:.2f}")

        # Reset transaction
        self.machine.current_payment = 0
        self.machine.selected_product = None

        # Return to idle state
        self.machine.change_state(IdleState())


# ============= VENDING MACHINE (CONTEXT) =============

class VendingMachine:
    """
    Vending Machine - the Context in State Pattern.
    Delegates actions to current state.
    """

    def __init__(self, inventory: Inventory):
        self.inventory = inventory
        self.current_payment = 0.0
        self.selected_product: Optional[Product] = None

        # Initialize with Idle state
        self.state = IdleState()
        self.state.set_machine(self)

    def change_state(self, new_state: VendingMachineState) -> None:
        """Change to a new state. This is the ONLY way states should change."""
        self.state = new_state
        self.state.set_machine(self)  # Give new state reference to machine

    # Public interface - delegates to current state
    def select_code(self, code: str) -> None:
        """Select a product by code."""
        self.state.select_code(code)

    def insert_money(self, amount: float) -> None:
        """Insert money."""
        self.state.insert_money(amount)

    def cancel_transaction(self) -> None:
        """Cancel current transaction."""
        self.state.cancel_transaction()

    def display_products(self) -> None:
        """Display all available products."""
        print("\n=== Vending Machine ===")
        print(f"{'Code':<8} {'Product':<15} {'Price':<10} {'In Stock':<10}")
        print("-" * 45)
        for product in self.inventory.products:
            status = f"{product.quantity}" if product.quantity > 0 else "Sold Out"
            print(
                f"{product.code:<8} {product.name:<15} ${product.price:<9.2f} {status}")
        print()

    def get_state_name(self) -> str:
        """Get current state name (for debugging)."""
        return self.state.get_state_name()


# ============= DEMO =============

def main():
    # Setup products
    products = [
        Product("A1", "Coke", 1.50, 10),
        Product("A2", "Pepsi", 1.50, 10),
        Product("A3", "Sprite", 1.50, 8),
        Product("B1", "Water", 1.00, 15),
        Product("B2", "Chips", 2.00, 5),
        Product("B3", "Candy", 1.25, 12)
    ]

    inventory = Inventory(products)
    vm = VendingMachine(inventory)

    print("Welcome to the Vending Machine!")
    vm.display_products()

    # Example 1: Simple purchase
    print("\n--- Example 1: Select A1 (Coke) ---")
    print(f"Current state: {vm.get_state_name()}")
    vm.select_code("A1")
    print(f"Current state: {vm.get_state_name()}")
    vm.insert_money(1.50)
    print(f"Current state: {vm.get_state_name()}")

    # Example 2: Insufficient funds
    print("\n--- Example 2: Select B2 (Chips) with insufficient funds ---")
    vm.select_code("B2")
    vm.insert_money(1.00)
    vm.insert_money(1.00)  # Now enough

    # Example 3: Cancel transaction
    print("\n--- Example 3: Cancel transaction ---")
    vm.select_code("A2")
    vm.insert_money(1.00)
    vm.cancel_transaction()
    print(f"Current state: {vm.get_state_name()}")

    # Final inventory
    print("\n--- Final Inventory ---")
    vm.display_products()


if __name__ == "__main__":
    main()
