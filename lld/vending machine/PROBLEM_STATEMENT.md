# Vending Machine - Low Level Design Problem

## Problem Statement

Design and implement a Vending Machine system that can handle product selection, payment processing, inventory management, and change dispensing. The system should follow object-oriented design principles and be extensible for future enhancements.

---

## Functional Requirements

### 1. Product Management
- The vending machine should support multiple products
- Each product has:
  - **Code**: Unique identifier (e.g., "A1", "B2", "C3")
  - **Name**: Product name (e.g., "Coke", "Chips")
  - **Price**: Price in dollars (e.g., $1.50)
  - **Quantity**: Available quantity in stock

### 2. User Interactions
- **Display Products**: Show all available products with codes, names, prices, and stock status
- **Select Product**: User can select a product by entering its code
- **Insert Money**: User can insert coins/bills to pay for the product
- **Cancel Transaction**: User can cancel a transaction at any time and receive a refund

### 3. Payment Processing
- Machine accepts common denominations: $0.01, $0.05, $0.10, $0.25, $0.50, $1.00, $2.00, $5.00, $10.00
- Track the total amount inserted by the user
- Verify if sufficient payment has been received before dispensing
- Calculate and return exact change when applicable
- If exact change cannot be returned, inform the user

### 4. Product Dispensing
- Dispense the selected product if:
  - Product is in stock
  - Sufficient payment has been received
- Update inventory after successful dispensing
- Display appropriate messages during the process

### 5. Change Management
- Machine has a coin/bill reserve for dispensing change
- Track available change denominations
- Return change using available denominations (greedy algorithm preferred)
- If exact change cannot be made, inform the user before dispensing

### 6. State Management
- The machine should operate in different states:
  - **Idle**: Ready to accept product selection
  - **Product Selected**: Product code entered, waiting for payment
  - **Payment In Progress**: Payment being collected
  - **Dispensing**: Product being dispensed
  - **Out of Stock**: Selected product is unavailable
  - **Insufficient Change**: Machine cannot provide exact change

---

## Non-Functional Requirements

1. **Extensibility**: Easy to add new product types or payment methods
2. **Maintainability**: Code should be well-structured and follow SOLID principles
3. **Error Handling**: Handle invalid codes, insufficient funds, out-of-stock scenarios gracefully
4. **Thread Safety**: Consider concurrent access if multiple users can interact simultaneously (optional)

---

## Design Constraints

1. Use **State Design Pattern** to manage different states of the vending machine
2. Use **Strategy Pattern** for payment processing (optional, for future extensibility)
3. Code should be modular and follow object-oriented principles
4. Each class should have a single responsibility
5. Use appropriate data structures (maps for product lookup, queues for change dispensation, etc.)

---

## Edge Cases to Handle

1. User selects an invalid product code
2. User selects a product that is out of stock
3. User inserts insufficient money
4. User cancels transaction mid-way
5. Machine runs out of change
6. User tries to select another product while one transaction is in progress
7. User tries to insert money before selecting a product (should it be allowed?)
8. Machine runs out of a specific denomination needed for change
9. Multiple rapid selections/cancellations
10. Exact change requirement (can machine always make exact change?)

---

## Example Interactions

### Scenario 1: Successful Purchase
```
1. User views products
2. User selects "A1" (Coke - $1.50)
3. User inserts $2.00
4. Machine dispenses Coke
5. Machine returns $0.50 change
```

### Scenario 2: Insufficient Funds
```
1. User selects "B2" (Chips - $2.00)
2. User inserts $1.00
3. Machine prompts: "Insufficient funds. Please insert $1.00 more."
4. User inserts $1.00
5. Machine dispenses Chips
```

### Scenario 3: Out of Stock
```
1. User selects "C3" (Product C3)
2. Machine displays: "Product C3 is out of stock. Please select another product."
```

### Scenario 4: Cancel Transaction
```
1. User selects "A1" (Coke - $1.50)
2. User inserts $1.00
3. User cancels transaction
4. Machine returns $1.00
5. Machine returns to Idle state
```

### Scenario 5: Insufficient Change
```
1. User selects "A1" (Coke - $1.50)
2. User inserts $5.00
3. Machine checks if it can provide $3.50 change
4. If insufficient change: "Machine cannot provide exact change. Transaction cancelled."
5. Machine returns $5.00
```

---

## Expected Deliverables

1. **Class Diagram** (optional, but recommended)
2. **Implementation** with:
   - State classes for different machine states
   - VendingMachine class
   - Product/Inventory management classes
   - Payment/Change handling classes
3. **Test Cases** demonstrating various scenarios
4. **Documentation** explaining design decisions

---

## Bonus Features (Optional)

1. Admin functionality to:
   - Restock products
   - Restock change denominations
   - View sales report
   - View inventory status

2. Support for multiple payment methods:
   - Cash
   - Credit Card (simplified)
   - Digital Wallet

3. Product categories (e.g., Drinks, Snacks, Healthy Options)

4. Product expiry tracking (if applicable)

---

## Questions to Consider

1. Should the machine allow inserting money before selecting a product?
2. What happens if the machine runs out of a product while user is in payment process?
3. Should partial payments be allowed across multiple transactions?
4. How should the machine prioritize change denominations when returning change?
5. Should there be a timeout for idle transactions?

---

## Success Criteria

Your implementation is successful if it:
- ✅ Handles all functional requirements
- ✅ Manages state transitions correctly
- ✅ Handles all edge cases gracefully
- ✅ Code is clean, maintainable, and follows OOP principles
- ✅ Uses appropriate design patterns
- ✅ Has clear separation of concerns

Good luck! 🎯

