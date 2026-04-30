'''
# HashMap Implementation - Low Level Design Problem

## Problem Statement

Design and implement a **HashMap (Hash Table)** data structure from scratch without using built-in dictionary/hashmap implementations. The HashMap should support basic key-value operations efficiently.

---

## Functional Requirements

### 1. Core Operations
- **`put(key, value)`**: Insert or update a key-value pair
- **`get(key)`**: Retrieve value for given key, return `None` if not found
- **`remove(key)`**: Remove key-value pair, return `True` if removed, `False` if key doesn't exist
- **`contains(key)`**: Check if key exists, return `True`/`False`

### 2. Additional Operations
- **`size()`**: Return number of key-value pairs
- **`is_empty()`**: Return `True` if empty, `False` otherwise

---

## Constraints

1. **No built-in hash structures**: Cannot use Python's `dict`, `set`, or any built-in hashmap
2. **Handle collisions**: Use chaining (linked list) or open addressing
3. **Dynamic resizing**: Resize when load factor exceeds threshold (e.g., 0.75)
4. **Key types**: Support string keys (or integers for simplicity)

---

## Example

```python
hm = HashMap()

hm.put("apple", 1)
hm.put("banana", 2)
hm.get("apple")      # Returns 1
hm.get("banana")     # Returns 2
hm.get("orange")     # Returns None
hm.contains("apple") # Returns True
hm.size()            # Returns 2
hm.remove("apple")   # Returns True
hm.size()            # Returns 1
```

---

## Design Considerations

1. **Hash Function**: Choose appropriate hash function for keys
2. **Bucket Array**: Use list/array to store buckets
3. **Collision Handling**: Implement chaining (list of key-value pairs per bucket)
4. **Load Factor**: Resize when `size / capacity > threshold`
5. **Rehashing**: Redistribute all keys when resizing

---

## Edge Cases

1. Inserting duplicate key (should update value)
2. Getting non-existent key
3. Removing non-existent key
4. Empty hashmap operations
5. Hash collisions (multiple keys hash to same bucket)
6. Large number of insertions (resizing)

---

## Expected Deliverables

1. **HashMap class** with all required methods
2. **Hash function** implementation
3. **Collision handling** (chaining)
4. **Dynamic resizing** logic
5. **Test cases** demonstrating:
   - Basic operations
   - Collision handling
   - Resizing behavior

---

## Success Criteria

- ✅ All operations work correctly
- ✅ Handles collisions properly
- ✅ Resizes when load factor threshold is reached
- ✅ O(1) average time complexity for operations
- ✅ Clean, maintainable code

---

**Time Limit**: ~45 minutes

**Hints**: Start with fixed-size array, then add resizing. Use list of lists for chaining.
'''

class HashMap:
    def __init__(self, capacity=191):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
    
    
    def _hash(self, key):
        return hash(key ) % self.capacity


    def _get_load_factor(self):
        return self.size() / self.capacity


    def _resize(self):
        tmp = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        for bucket in tmp:
            for k,v in bucket:
                hashed_key = self._hash(k)
                self.buckets[hashed_key].append((k,v))

    
    def put(self, key, value):
        hashed_key = self._hash(key)
        bucket = self.buckets[hashed_key]
        for i, (k, v ) in enumerate(bucket):
            if k == key:
                bucket[i] = (key,value) # override the value
                return
        bucket.append((key,value))
        if self._get_load_factor() > 0.75:
            self._resize()


    def get(self, key):
        hashed_key = self._hash(key)
        bucket = self.buckets[hashed_key]
        for k, v in bucket:
            if k == key:
                return v
        return None


    def remove(self, key):
        hashed_key = self._hash(key)
        bucket = self.buckets[hashed_key]
        for i, (k,v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False


    def contains(self, key):
        hashed_key = self._hash(key)
        bucket = self.buckets[hashed_key]
        for k, v in bucket:
            if k == key:
                return True
        return False


    def size(self):
        length = 0
        for bucket in self.buckets:
            length += len(bucket)
        return length


    def is_empty(self):
        return self.size() == 0


if __name__ == "__main__":
    print("=" * 60)
    print("HASHMAP TEST SUITE")
    print("=" * 60)
    
    # Test 1: Basic Operations
    print("\n--- Test 1: Basic Operations ---")
    hm = HashMap()
    hm.put("apple", 1)
    hm.put("banana", 2)
    assert hm.get("apple") == 1, "Should return 1"
    assert hm.get("banana") == 2, "Should return 2"
    assert hm.get("orange") is None, "Should return None"
    assert hm.contains("apple") is True, "Should return True"
    assert hm.size() == 2, "Size should be 2"
    assert hm.remove("apple") is True, "Should return True"
    assert hm.size() == 1, "Size should be 1"
    print("✓ Basic operations: PASSED")
    
    # Test 2: Load Factor Calculation
    print("\n--- Test 2: Load Factor Calculation ---")
    hm = HashMap(capacity=10)
    assert hm.size() == 0, "Initial size should be 0"
    # Note: You'll need to expose _get_load_factor or calculate it in test
    # load_factor = hm.size() / hm.capacity
    # assert load_factor == 0.0, "Initial load factor should be 0.0"
    
    hm.put("a", 1)
    load_factor = hm.size() / hm.capacity
    assert load_factor == 0.1, f"Load factor should be 0.1, got {load_factor}"
    print(f"✓ Load factor with 1 item: {load_factor}")
    
    for i in range(2, 8):
        hm.put(f"key{i}", i)
    load_factor = hm.size() / hm.capacity
    assert load_factor == 0.7, f"Load factor should be 0.7, got {load_factor}"
    print(f"✓ Load factor with 7 items: {load_factor}")
    
    # Test 3: Resizing Trigger
    print("\n--- Test 3: Resizing Trigger ---")
    hm = HashMap(capacity=10)
    initial_capacity = hm.capacity
    
    # Insert items until load factor exceeds 0.75
    for i in range(8):  # 8/10 = 0.8 > 0.75
        hm.put(f"key{i}", i)
    
    # Check if resize was triggered
    if hm.capacity > initial_capacity:
        print(f"✓ Resize triggered: capacity {initial_capacity} → {hm.capacity}")
        assert hm.capacity == initial_capacity * 2, "Capacity should double"
    else:
        print(f"⚠ Resize not triggered yet (capacity: {hm.capacity})")
    
    # Verify all items still accessible after resize
    for i in range(8):
        assert hm.get(f"key{i}") == i, f"Key key{i} should still be accessible"
    print("✓ All items accessible after resize")
    
    # Test 4: Multiple Resizes
    print("\n--- Test 4: Multiple Resizes ---")
    hm = HashMap(capacity=4)  # Small initial capacity
    capacities = [hm.capacity]
    
    # Insert many items to trigger multiple resizes
    for i in range(20):
        hm.put(f"key{i}", i)
        if hm.capacity != capacities[-1]:
            capacities.append(hm.capacity)
            print(f"  Resize at size {hm.size()}: capacity {capacities[-2]} → {capacities[-1]}")
    
    assert len(capacities) > 1, "Should have triggered at least one resize"
    print(f"✓ Multiple resizes occurred: {capacities}")
    
    # Verify all items still accessible
    for i in range(20):
        assert hm.get(f"key{i}") == i, f"Key key{i} should be accessible"
    print("✓ All 20 items accessible after multiple resizes")
    
    # Test 5: Load Factor After Resize
    print("\n--- Test 5: Load Factor After Resize ---")
    hm = HashMap(capacity=10)
    
    # Fill to trigger resize
    for i in range(8):
        hm.put(f"key{i}", i)
    
    load_factor_after = hm.size() / hm.capacity
    print(f"✓ Load factor after resize: {load_factor_after:.2f}")
    assert load_factor_after < 0.75, "Load factor should be below threshold after resize"
    
    # Test 6: Rehashing - Keys in Correct Buckets
    print("\n--- Test 6: Rehashing - Keys in Correct Buckets ---")
    hm = HashMap(capacity=5)
    
    # Insert items
    test_keys = ["a", "b", "c", "d", "e", "f"]
    for key in test_keys:
        hm.put(key, ord(key))
    
    # After potential resize, verify keys are correctly hashed
    for key in test_keys:
        expected_value = ord(key)
        assert hm.get(key) == expected_value, f"Key {key} should map to {expected_value}"
    print("✓ All keys correctly rehashed and accessible")
    
    # Test 7: Update Existing Key After Resize
    print("\n--- Test 7: Update Existing Key After Resize ---")
    hm = HashMap(capacity=5)
    
    hm.put("apple", 1)
    hm.put("banana", 2)
    
    # Trigger resize
    for i in range(5):
        hm.put(f"key{i}", i)
    
    # Update existing key after resize
    hm.put("apple", 100)
    assert hm.get("apple") == 100, "Should update to 100"
    assert hm.get("banana") == 2, "Should still be 2"
    print("✓ Update existing key after resize works")
    
    # Test 8: Remove After Resize
    print("\n--- Test 8: Remove After Resize ---")
    hm = HashMap(capacity=5)
    
    keys = ["a", "b", "c", "d", "e", "f", "g"]
    for key in keys:
        hm.put(key, ord(key))
    
    initial_size = hm.size()
    assert hm.remove("a") is True, "Should remove successfully"
    assert hm.size() == initial_size - 1, "Size should decrease"
    assert hm.get("a") is None, "Should return None after removal"
    print("✓ Remove works correctly after resize")
    
    # Test 9: Load Factor Threshold Edge Cases
    print("\n--- Test 9: Load Factor Threshold Edge Cases ---")
    hm = HashMap(capacity=10)
    
    # Insert 7 items (0.7 load factor - below threshold)
    for i in range(7):
        hm.put(f"key{i}", i)
    assert hm.size() / hm.capacity == 0.7, "Load factor should be 0.7"
    print("✓ Load factor 0.7 (below threshold): OK")
    
    # Insert 8th item (0.8 load factor - above threshold)
    hm.put("key7", 7)
    load_factor = hm.size() / hm.capacity
    print(f"✓ Load factor after 8th item: {load_factor:.2f}")
    
    # Test 10: Large Scale Test
    print("\n--- Test 10: Large Scale Test ---")
    hm = HashMap(capacity=16)
    
    # Insert 100 items
    for i in range(100):
        hm.put(f"key{i}", i)
    
    assert hm.size() == 100, "Should have 100 items"
    final_load_factor = hm.size() / hm.capacity
    print(f"✓ Final capacity: {hm.capacity}, Load factor: {final_load_factor:.2f}")
    
    # Verify all items
    for i in range(100):
        assert hm.get(f"key{i}") == i, f"Key key{i} should be accessible"
    print("✓ All 100 items accessible")
    
    # Test 11: Collision Handling After Resize
    print("\n--- Test 11: Collision Handling After Resize ---")
    hm = HashMap(capacity=5)
    
    # Insert items that might collide
    collision_keys = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for key in collision_keys:
        hm.put(key, ord(key))
    
    # After resize, all should still work
    for key in collision_keys:
        assert hm.get(key) == ord(key), f"Key {key} should work after resize"
    print("✓ Collision handling works after resize")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED! ✓")
    print("=" * 60)