'''
 Shopping Cart - Low Level Design Problem

## Problem Statement

Design and implement a **Shopping Cart** system that allows users to add products, view cart contents, and checkout. The system should handle product management, cart constraints, and provide descriptive error handling for edge cases.

---

## Functional Requirements

### 1. Product Management
- Each product has:
  - **Product ID**: Unique identifier
  - **Name**: Product name
  - **Price**: Unit price (positive number)
  - **Quantity Available**: Stock quantity

### 2. Core Cart Operations
- **Add Item**: Add product to cart with quantity
- **View Cart**: Display all items in cart with details (product name, quantity, price, subtotal)
- **Checkout**: Process cart and clear it (optional: calculate total)

### 3. Cart Constraints
- **Cart Size Limit**: Maximum number of items/cart capacity (e.g., 10 items)
- **Stock Validation**: Cannot add more items than available in stock
- **Empty Cart**: Cannot checkout with empty cart

### 4. Exception Handling
The system must handle and return descriptive errors for:
- **Item Out of Stock**: When trying to add item with insufficient stock
- **Cart is Full**: When cart reaches maximum capacity
- **Checkout with Empty Cart**: When attempting checkout with no items
- **Invalid Product**: When product ID doesn't exist
- **Invalid Quantity**: When quantity is <= 0

---

## Example

```python
cart = ShoppingCart(max_size=10)

# Add products
cart.add_item("P001", 2)  # Add 2 units of product P001
cart.add_item("P002", 1)  # Add 1 unit of product P002

# View cart
cart.view_cart()  
# Output:
# Product: Apple, Quantity: 2, Price: $1.50, Subtotal: $3.00
# Product: Banana, Quantity: 1, Price: $0.50, Subtotal: $0.50
# Total: $3.50

# Checkout
cart.checkout()  # Processes and clears cart

# Try to checkout empty cart
cart.checkout()  # Raises EmptyCartException
```

---

## Design Constraints

1. **Object-Oriented Design**: Use classes for Cart and Product
2. **Data Structure**: Use dictionary (`{product_id: quantity}`) to store cart items for O(1) lookups
3. **Cart Size Limits**: Enforce maximum cart capacity
4. **Exception Handling**: Use custom exceptions with descriptive messages
5. **Error Messages**: Return clear, descriptive error messages

---

## Expected Classes

1. **Product**: Represents a product with ID, name, price, stock
2. **ShoppingCart**: Manages cart operations and constraints
   - Uses dictionary to store items: `{product_id: quantity}`
   - No need for separate CartItem class (keep it simple)
3. **Custom Exceptions**:
   - `OutOfStockException`
   - `CartFullException`
   - `EmptyCartException`
   - `InvalidProductException`

---

## Design Note

**Cart Storage**: Use a simple dictionary structure `{product_id: quantity}` in the ShoppingCart class. This is:
- Simple and efficient (O(1) lookups)
- Sufficient for basic requirements
- Easy to extend if needed later
- No need for a separate CartItem class for basic implementation

---

## Edge Cases to Handle

1. **Item Out of Stock**: User tries to add 5 items but only 3 available
2. **Cart is Full**: Cart has 10 items, trying to add 11th
3. **Checkout Empty Cart**: User tries to checkout with no items
4. **Invalid Product ID**: Product doesn't exist
5. **Invalid Quantity**: Quantity <= 0 or negative
6. **Adding Duplicate Product**: Update quantity vs new entry
7. **Exceeding Cart Limit**: Adding item that would exceed max size

---

## Example Error Messages

```python
# Out of Stock
"Error: Product 'P001' (Apple) is out of stock. Available: 0, Requested: 2"

# Cart Full
"Error: Cart is full. Maximum capacity: 10 items. Current: 10 items"

# Empty Cart Checkout
"Error: Cannot checkout empty cart. Please add items first."

# Invalid Product
"Error: Product 'P999' not found."

# Invalid Quantity
"Error: Quantity must be greater than 0. Provided: -1"
```

---

## Success Criteria

- ✅ All cart operations work correctly
- ✅ Cart size limits are enforced
- ✅ Stock validation works
- ✅ Descriptive error messages for all exceptions
- ✅ Clean, maintainable OOP design
- ✅ Handles all edge cases gracefully

---

**Time Limit**: ~45 minutes

**Domain Focus**: This is a domain-focused design question. Focus on:
- Clear object-oriented design (Product, Cart classes)
- Simple data structure (dict for cart items)
- Proper exception handling
- Descriptive error messages
- Cart constraints and validation

'''
import uuid
from threading import Lock

class Product:
    def __init__(self, product_id, product_name, price):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price

    def __repr__(self):
        return f"Product(id={self.product_id}, product_name={self.product_name}, price={self.price})"

class Inventory:
    def __init__(self):
        self.products_count = {}
        self.products = {}
        self._lock = Lock()

    def add_product(self, product, quantity):
        self.products_count[product.product_id] = self.products_count.get(product.product_id, 0) + quantity
        self.products[product.product_id] = product

    
    def get_product(self, product_id):
        try:
            return self.products[product_id]
        except KeyError:
            raise InvalidProductException(product_id)

    
    def reserve(self, product_id, quantity):
        if quantity <= 0:
            raise InvalidQuantityException()
        with self._lock:
            if product_id not in self.products_count:
                raise InvalidProductException(product_id)
            if self.products_count[product_id] < quantity:
                raise OutOfStockException(quantity, self.products_count[product_id], self.products[product_id].product_name)
            self.products_count[product_id] -= quantity

    def release(self, product_id, quantity):
        with self._lock:
            if product_id not in self.products_count:
                raise InvalidProductException(product_id)
            self.products_count[product_id] += quantity            



class Cart:
    def __init__(self, max_size, inventory):
        self.id = uuid.uuid4()
        self.max_size = max_size
        self.items = {}
        self.inventory = inventory

    def _current_size(self):
        return sum(self.items.values())

    def add_item(self, product_id, quantity):
        if self._current_size() + quantity > self.max_size:
            raise CartFullException(self.max_size, self._current_size() + quantity)
        try:
            self.inventory.reserve(product_id, quantity)
        except InvalidProductException as e:
            raise e
        except OutOfStockException as e:
            raise e 
        self.items[product_id] = self.items.get(product_id, 0) + quantity


    def remove_item(self, product_id, quantity):
        if product_id not in self.items:
            raise InvalidProductException(product_id)
        if self.items[product_id] < quantity:
            raise InvalidQuantityException()
        self.items[product_id] -= quantity
        if self.items[product_id] == 0:
            del self.items[product_id]
        self.inventory.release(product_id, quantity)


    def view_cart(self):
        for product_id, quantity in self.items.items():
            product = self.inventory.get_product(product_id)
            print(f"Product: {product.product_name}, Quantity: {quantity}, Price: {product.price}, Subtotal: {product.price * quantity}")

    def get_total(self):
        total = 0
        for product_id, quantity in self.items.items():
            product = self.inventory.get_product(product_id)
            total += product.price * quantity
        return total

    def checkout(self):
        total_amount = self.get_total()
        if self._current_size() == 0:
            raise EmptyCartException()
        self.items.clear()
        return total_amount

class OutOfStockException(Exception):
    def __init__(self, quantity_requested, quantity_avaialble, product_name):
        super().__init__(f"Product {product_name} is out of stock. Requested: {quantity_requested}")

class InvalidProductException(Exception):
    def __init__(self, product_id):
        super().__init__(f'Product {product_id} not found')

class InvalidQuantityException(Exception):
    def __init__(self):
        super().__init__('Invalid quantity requested')

class CartFullException(Exception):
    def __init__(self, max_size, current_size):
        super().__init__(f"Cart is full. Maximum capacity: {max_size} items. Current: {current_size} items")

class EmptyCartException(Exception):
    def __init__(self):
        super().__init__("Cart is empty, can't checkout")