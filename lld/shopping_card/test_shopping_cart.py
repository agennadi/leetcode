"""
Comprehensive test suite for Shopping Cart implementation
"""
import sys
import os

# Import the shopping cart classes
from shopping_card import (
    Product, Inventory, Cart,
    OutOfStockException, InvalidProductException, InvalidQuantityException,
    CartFullException, EmptyCartException
)

def test_basic_add_and_view():
    """Test basic add item and view cart functionality"""
    print("\n=== Test 1: Basic Add and View ===")
    try:
        inventory = Inventory()
        product1 = Product("P001", "Apple", 1.50)
        product2 = Product("P002", "Banana", 0.50)
        
        inventory.add_product(product1, 10)
        inventory.add_product(product2, 20)
        
        cart = Cart(max_size=10, inventory=inventory)
        cart.add_item("P001", 2)
        cart.add_item("P002", 3)
        
        assert cart.items["P001"] == 2
        assert cart.items["P002"] == 3
        expected_total = (2 * 1.50) + (3 * 0.50)
        assert abs(cart.get_total() - expected_total) < 0.01
        print("✅ Test 1 PASSED: Basic add and view")
    except Exception as e:
        print(f"❌ Test 1 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_out_of_stock():
    """Test out of stock exception"""
    print("\n=== Test 2: Out of Stock ===")
    try:
        inventory = Inventory()
        product = Product("P001", "Apple", 1.50)
        inventory.add_product(product, 5)
        
        cart = Cart(max_size=10, inventory=inventory)
        cart.add_item("P001", 3)  # Reserve 3, leaves 2
        
        try:
            cart.add_item("P001", 5)  # Should fail - only 2 left
            print("❌ Test 2 FAILED: Should have raised OutOfStockException")
        except OutOfStockException as e:
            print(f"✅ Test 2 PASSED: {e}")
        except Exception as e:
            print(f"❌ Test 2 FAILED: Wrong exception: {type(e).__name__}: {e}")
    except Exception as e:
        print(f"❌ Test 2 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_invalid_product():
    """Test invalid product exception"""
    print("\n=== Test 3: Invalid Product ===")
    try:
        inventory = Inventory()
        cart = Cart(max_size=10, inventory=inventory)
        
        try:
            cart.add_item("P999", 1)  # Product doesn't exist
            print("❌ Test 3 FAILED: Should have raised InvalidProductException")
        except InvalidProductException as e:
            print(f"✅ Test 3 PASSED: {e}")
        except Exception as e:
            print(f"❌ Test 3 FAILED: Wrong exception: {type(e).__name__}: {e}")
    except Exception as e:
        print(f"❌ Test 3 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_cart_full():
    """Test cart full exception (total quantity limit)"""
    print("\n=== Test 4: Cart Full (Total Quantity Limit) ===")
    try:
        inventory = Inventory()
        product1 = Product("P001", "Apple", 1.50)
        product2 = Product("P002", "Banana", 0.50)
        
        inventory.add_product(product1, 100)
        inventory.add_product(product2, 100)
        
        cart = Cart(max_size=5, inventory=inventory)  # Max 5 total items
        cart.add_item("P001", 3)  # 3 items
        
        try:
            cart.add_item("P002", 3)  # Should fail - 3 + 3 = 6 > 5
            print("❌ Test 4 FAILED: Should have raised CartFullException")
        except CartFullException as e:
            print(f"✅ Test 4 PASSED: {e}")
        except Exception as e:
            print(f"❌ Test 4 FAILED: Wrong exception: {type(e).__name__}: {e}")
    except Exception as e:
        print(f"❌ Test 4 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_cart_full_exact_limit():
    """Test cart full at exact limit"""
    print("\n=== Test 5: Cart Full at Exact Limit ===")
    try:
        inventory = Inventory()
        product = Product("P001", "Apple", 1.50)
        inventory.add_product(product, 100)
        
        cart = Cart(max_size=5, inventory=inventory)
        cart.add_item("P001", 5)  # Exactly at limit
        
        assert cart._current_size() == 5
        assert len(cart.items) == 1
        
        try:
            cart.add_item("P001", 1)  # Should fail - 5 + 1 = 6 > 5
            print("❌ Test 5 FAILED: Should have raised CartFullException")
        except CartFullException as e:
            print(f"✅ Test 5 PASSED: {e}")
        except Exception as e:
            print(f"❌ Test 5 FAILED: Wrong exception: {type(e).__name__}: {e}")
    except Exception as e:
        print(f"❌ Test 5 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_empty_cart_checkout():
    """Test empty cart checkout exception"""
    print("\n=== Test 6: Empty Cart Checkout ===")
    try:
        inventory = Inventory()
        cart = Cart(max_size=10, inventory=inventory)
        
        try:
            cart.checkout()
            print("❌ Test 6 FAILED: Should have raised EmptyCartException")
        except EmptyCartException as e:
            print(f"✅ Test 6 PASSED: {e}")
        except Exception as e:
            print(f"❌ Test 6 FAILED: Wrong exception: {type(e).__name__}: {e}")
    except Exception as e:
        print(f"❌ Test 6 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_remove_item():
    """Test remove item functionality"""
    print("\n=== Test 7: Remove Item ===")
    try:
        inventory = Inventory()
        product = Product("P001", "Apple", 1.50)
        inventory.add_product(product, 10)
        
        cart = Cart(max_size=10, inventory=inventory)
        cart.add_item("P001", 5)
        assert inventory.products_count["P001"] == 5  # 10 - 5 = 5
        
        cart.remove_item("P001", 2)
        assert cart.items["P001"] == 3
        assert inventory.products_count["P001"] == 7  # 5 + 2 = 7
        
        cart.remove_item("P001", 3)
        assert "P001" not in cart.items
        assert inventory.products_count["P001"] == 10  # 7 + 3 = 10 (back to original)
        
        print("✅ Test 7 PASSED: Remove item works correctly")
    except Exception as e:
        print(f"❌ Test 7 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_remove_item_invalid_quantity():
    """Test removing more items than in cart"""
    print("\n=== Test 8: Remove Item - Invalid Quantity ===")
    try:
        inventory = Inventory()
        product = Product("P001", "Apple", 1.50)
        inventory.add_product(product, 10)
        
        cart = Cart(max_size=10, inventory=inventory)
        cart.add_item("P001", 3)
        
        try:
            cart.remove_item("P001", 5)  # Only 3 in cart
            print("❌ Test 8 FAILED: Should have raised InvalidQuantityException")
        except InvalidQuantityException as e:
            print(f"✅ Test 8 PASSED: {e}")
        except Exception as e:
            print(f"❌ Test 8 FAILED: Wrong exception: {type(e).__name__}: {e}")
    except Exception as e:
        print(f"❌ Test 8 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_remove_item_not_in_cart():
    """Test removing item that's not in cart"""
    print("\n=== Test 9: Remove Item - Not in Cart ===")
    try:
        inventory = Inventory()
        cart = Cart(max_size=10, inventory=inventory)
        
        try:
            cart.remove_item("P999", 1)  # Product not in cart
            print("❌ Test 9 FAILED: Should have raised InvalidProductException")
        except InvalidProductException as e:
            print(f"✅ Test 9 PASSED: {e}")
        except Exception as e:
            print(f"❌ Test 9 FAILED: Wrong exception: {type(e).__name__}: {e}")
    except Exception as e:
        print(f"❌ Test 9 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_invalid_quantity_add():
    """Test invalid quantity when adding (zero or negative)"""
    print("\n=== Test 10: Invalid Quantity - Add ===")
    try:
        inventory = Inventory()
        product = Product("P001", "Apple", 1.50)
        inventory.add_product(product, 10)
        
        cart = Cart(max_size=10, inventory=inventory)
        
        try:
            cart.add_item("P001", 0)  # Should fail
            print("❌ Test 10 FAILED: Should have raised InvalidQuantityException for 0")
        except InvalidQuantityException as e:
            print(f"✅ Test 10 PASSED (zero): {e}")
        except Exception as e:
            print(f"❌ Test 10 FAILED: Wrong exception: {type(e).__name__}: {e}")
        
        try:
            cart.add_item("P001", -1)  # Should fail
            print("❌ Test 10 FAILED: Should have raised InvalidQuantityException for negative")
        except InvalidQuantityException as e:
            print(f"✅ Test 10 PASSED (negative): {e}")
        except Exception as e:
            print(f"❌ Test 10 FAILED: Wrong exception: {type(e).__name__}: {e}")
    except Exception as e:
        print(f"❌ Test 10 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_add_existing_item():
    """Test adding more quantity to existing item in cart"""
    print("\n=== Test 11: Add to Existing Item ===")
    try:
        inventory = Inventory()
        product = Product("P001", "Apple", 1.50)
        inventory.add_product(product, 20)
        
        cart = Cart(max_size=10, inventory=inventory)
        cart.add_item("P001", 2)
        assert cart.items["P001"] == 2
        
        cart.add_item("P001", 3)  # Add more to existing
        assert cart.items["P001"] == 5
        expected_total = 5 * 1.50
        assert abs(cart.get_total() - expected_total) < 0.01
        
        print("✅ Test 11 PASSED: Adding to existing item works")
    except Exception as e:
        print(f"❌ Test 11 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_checkout():
    """Test checkout functionality"""
    print("\n=== Test 12: Checkout ===")
    try:
        inventory = Inventory()
        product1 = Product("P001", "Apple", 1.50)
        product2 = Product("P002", "Banana", 0.50)
        
        inventory.add_product(product1, 10)
        inventory.add_product(product2, 10)
        
        cart = Cart(max_size=10, inventory=inventory)
        cart.add_item("P001", 2)
        cart.add_item("P002", 3)
        
        total = cart.checkout()
        assert total == 4.50
        assert len(cart.items) == 0
        assert cart._current_size() == 0
        
        print(f"✅ Test 12 PASSED: Checkout total = ${total}")
    except Exception as e:
        print(f"❌ Test 12 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_get_total():
    """Test get_total calculation"""
    print("\n=== Test 13: Get Total ===")
    try:
        inventory = Inventory()
        product1 = Product("P001", "Apple", 1.50)
        product2 = Product("P002", "Banana", 0.50)
        product3 = Product("P003", "Orange", 2.00)
        
        inventory.add_product(product1, 100)
        inventory.add_product(product2, 100)
        inventory.add_product(product3, 100)
        
        cart = Cart(max_size=20, inventory=inventory)
        cart.add_item("P001", 3)
        cart.add_item("P002", 2)
        cart.add_item("P003", 1)
        
        expected_total = (3 * 1.50) + (2 * 0.50) + (1 * 2.00)
        assert abs(cart.get_total() - expected_total) < 0.01  # Use approximate comparison for floats
        
        print(f"✅ Test 13 PASSED: Total = ${cart.get_total()}")
    except Exception as e:
        print(f"❌ Test 13 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_multiple_operations():
    """Test multiple operations in sequence"""
    print("\n=== Test 14: Multiple Operations ===")
    try:
        inventory = Inventory()
        product1 = Product("P001", "Apple", 1.50)
        product2 = Product("P002", "Banana", 0.50)
        product3 = Product("P003", "Orange", 2.00)
        
        inventory.add_product(product1, 100)
        inventory.add_product(product2, 100)
        inventory.add_product(product3, 100)
        
        cart = Cart(max_size=20, inventory=inventory)
        
        # Add items
        cart.add_item("P001", 2)
        cart.add_item("P002", 1)
        cart.add_item("P001", 1)  # Add more to existing
        cart.add_item("P003", 2)
        
        assert cart.items["P001"] == 3
        assert cart.items["P002"] == 1
        assert cart.items["P003"] == 2
        expected_total1 = (3 * 1.50) + (1 * 0.50) + (2 * 2.00)
        assert abs(cart.get_total() - expected_total1) < 0.01
        
        # Remove items
        cart.remove_item("P001", 1)
        assert cart.items["P001"] == 2
        expected_total2 = (2 * 1.50) + (1 * 0.50) + (2 * 2.00)
        assert abs(cart.get_total() - expected_total2) < 0.01
        
        # Remove all of one product
        cart.remove_item("P002", 1)
        assert "P002" not in cart.items
        assert cart.items["P001"] == 2
        assert cart.items["P003"] == 2
        
        print("✅ Test 14 PASSED: Multiple operations work correctly")
    except Exception as e:
        print(f"❌ Test 14 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_stock_tracking():
    """Test stock tracking after reserve and release"""
    print("\n=== Test 15: Stock Tracking ===")
    try:
        inventory = Inventory()
        product = Product("P001", "Apple", 1.50)
        inventory.add_product(product, 10)
        
        assert inventory.products_count["P001"] == 10
        
        cart = Cart(max_size=10, inventory=inventory)
        cart.add_item("P001", 3)  # Reserve 3
        assert inventory.products_count["P001"] == 7  # 10 - 3 = 7
        
        cart.add_item("P001", 2)  # Reserve 2 more
        assert inventory.products_count["P001"] == 5  # 7 - 2 = 5
        
        cart.remove_item("P001", 1)  # Release 1
        assert inventory.products_count["P001"] == 6  # 5 + 1 = 6
        
        cart.remove_item("P001", 4)  # Release 4 more
        assert inventory.products_count["P001"] == 10  # 6 + 4 = 10 (back to original)
        
        print("✅ Test 15 PASSED: Stock tracking works correctly")
    except Exception as e:
        print(f"❌ Test 15 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_view_cart():
    """Test view_cart output"""
    print("\n=== Test 16: View Cart ===")
    try:
        inventory = Inventory()
        product1 = Product("P001", "Apple", 1.50)
        product2 = Product("P002", "Banana", 0.50)
        
        inventory.add_product(product1, 10)
        inventory.add_product(product2, 10)
        
        cart = Cart(max_size=10, inventory=inventory)
        cart.add_item("P001", 2)
        cart.add_item("P002", 3)
        
        print("Cart view output:")
        cart.view_cart()
        print("✅ Test 16 PASSED: View cart displays correctly")
    except Exception as e:
        print(f"❌ Test 16 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_get_product():
    """Test get_product from inventory"""
    print("\n=== Test 17: Get Product ===")
    try:
        inventory = Inventory()
        product = Product("P001", "Apple", 1.50)
        inventory.add_product(product, 10)
        
        retrieved_product = inventory.get_product("P001")
        assert retrieved_product.product_id == "P001"
        assert retrieved_product.product_name == "Apple"
        assert retrieved_product.price == 1.50
        
        try:
            inventory.get_product("P999")  # Doesn't exist
            print("❌ Test 17 FAILED: Should have raised InvalidProductException")
        except InvalidProductException:
            print("✅ Test 17 PASSED: Get product works correctly")
    except Exception as e:
        print(f"❌ Test 17 FAILED: {e}")
        import traceback
        traceback.print_exc()

def test_cart_with_different_products():
    """Test cart with multiple different products"""
    print("\n=== Test 18: Cart with Multiple Products ===")
    try:
        inventory = Inventory()
        products = [
            Product("P001", "Apple", 1.50),
            Product("P002", "Banana", 0.50),
            Product("P003", "Orange", 2.00),
            Product("P004", "Grape", 3.00)
        ]
        
        for product in products:
            inventory.add_product(product, 100)
        
        cart = Cart(max_size=20, inventory=inventory)
        cart.add_item("P001", 1)
        cart.add_item("P002", 2)
        cart.add_item("P003", 3)
        cart.add_item("P004", 1)
        
        assert len(cart.items) == 4
        assert cart._current_size() == 7
        expected_total3 = (1 * 1.50) + (2 * 0.50) + (3 * 2.00) + (1 * 3.00)
        assert abs(cart.get_total() - expected_total3) < 0.01
        
        print("✅ Test 18 PASSED: Multiple products handled correctly")
    except Exception as e:
        print(f"❌ Test 18 FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 70)
    print("SHOPPING CART COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    test_basic_add_and_view()
    test_out_of_stock()
    test_invalid_product()
    test_cart_full()
    test_cart_full_exact_limit()
    test_empty_cart_checkout()
    test_remove_item()
    test_remove_item_invalid_quantity()
    test_remove_item_not_in_cart()
    test_invalid_quantity_add()
    test_add_existing_item()
    test_checkout()
    test_get_total()
    test_multiple_operations()
    test_stock_tracking()
    test_view_cart()
    test_get_product()
    test_cart_with_different_products()
    
    print("\n" + "=" * 70)
    print("TEST SUITE COMPLETE")
    print("=" * 70)

