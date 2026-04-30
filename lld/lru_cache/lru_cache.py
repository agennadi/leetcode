'''
LRU Cache - Low Level Design Problem

## Problem Statement

Design and implement a **Least Recently Used (LRU) Cache** data structure that supports `get` and `put` operations with O(1) time complexity. The cache should evict the least recently used item when the capacity is reached.

---

## Functional Requirements

### 1. Core Operations

- **`get(key)`**: Retrieve the value of the key if it exists, otherwise return -1 (or None)
  - When accessed, the key becomes the most recently used
  - Time complexity: O(1)

- **`put(key, value)`**: Insert or update the key-value pair
  - If the key exists, update its value and mark it as most recently used
  - If the key doesn't exist and cache is at capacity, evict the least recently used item, then add the new item
  - If the key doesn't exist and cache has space, add the new item
  - Time complexity: O(1)

### 2. Cache Constraints

- **Fixed Capacity**: Cache has a maximum capacity (e.g., 2, 10, 100)
- **Eviction Policy**: When capacity is reached and a new item is added, remove the least recently used item
- **Access Ordering**: Every `get` or `put` operation updates the "most recently used" status

---

## Example

```python
cache = LRUCache(2)  # Capacity of 2

# Put operations
cache.put(1, 1)      # Cache: {1: 1}
cache.put(2, 2)      # Cache: {1: 1, 2: 2}

# Get operation
cache.get(1)         # Returns 1, Cache: {2: 2, 1: 1} (1 becomes most recent)

# Put when at capacity - evicts least recent (2)
cache.put(3, 3)      # Cache: {1: 1, 3: 3} (2 is evicted)

# Get for evicted key
cache.get(2)         # Returns -1 (not found)

# Update existing key
cache.put(1, 10)     # Cache: {3: 3, 1: 10} (updates 1, makes it most recent)

# Get operation
cache.get(1)         # Returns 10
```

---

## Design Constraints

1. **Time Complexity**: Both `get` and `put` operations must be O(1)
2. **Space Complexity**: O(capacity) - cache stores at most `capacity` items
3. **Data Structures**: Use appropriate data structures (hint: combination of HashMap and Doubly Linked List)
4. **No Built-in Ordered Dict**: Do not use Python's `OrderedDict` or similar built-in ordered structures
5. **Thread Safety**: Not required for this problem

---

## Expected Data Structure

The solution typically requires:
- **HashMap/Dictionary**: For O(1) key lookup
- **Doubly Linked List**: For O(1) insertion, deletion, and reordering
- **Node Class**: To represent cache entries with key, value, prev, next pointers

---

## Edge Cases to Handle

1. **Cache at Capacity**: Adding new item when cache is full
2. **Updating Existing Key**: Updating value of existing key (should update recency)
3. **Getting Non-existent Key**: Return -1 or None
4. **Single Item Cache**: Cache with capacity 1
5. **Repeated Access**: Same key accessed multiple times
6. **Capacity Zero**: Cache with capacity 0 (optional edge case)

---

## Example Test Cases

```python
# Test Case 1: Basic operations
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
assert cache.get(1) == 1
cache.put(3, 3)  # Evicts key 2
assert cache.get(2) == -1
assert cache.get(3) == 3

# Test Case 2: Update existing key
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
cache.put(1, 10)  # Updates key 1, makes it most recent
assert cache.get(1) == 10
cache.put(3, 3)  # Evicts key 2 (1 is most recent)
assert cache.get(2) == -1
assert cache.get(1) == 10

# Test Case 3: Capacity 1
cache = LRUCache(1)
cache.put(1, 1)
cache.put(2, 2)  # Evicts 1
assert cache.get(1) == -1
assert cache.get(2) == 2
```

---

## Success Criteria

- ✅ `get` and `put` operations work correctly
- ✅ O(1) time complexity for both operations
- ✅ Correct eviction of least recently used item
- ✅ Proper handling of updating existing keys
- ✅ All edge cases handled correctly
- ✅ Clean, maintainable code structure

---

## Design Patterns & Concepts

- **Doubly Linked List**: For efficient insertion/deletion
- **HashMap**: For O(1) key lookup
- **Node-based Design**: Encapsulate key-value pairs in nodes

---

**Time Limit**: ~45-60 minutes

**Difficulty**: Medium

'''

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.dummy_head = Node(None, None)
        self.dummy_tail = Node(None, None)
        self.dummy_head.next = self.dummy_tail
        self.dummy_tail.prev = self.dummy_head
        self.lookup = {}
    
    def _add_to_head(self, node):
        node.prev = self.dummy_head # new node points back to dummy_head
        node.next = self.dummy_head.next # new node points forward to the current first real node

        self.dummy_head.next.prev = node # current first real node points back to the new node
        self.dummy_head.next = node # dummy head points forwarf to the new node

    
    def _pop_from_tail(self):
        last_node = self.dummy_tail.prev # get the last real node that is about to be evicted
        self._remove_node(last_node) 
        return last_node


    def _remove_node(self, node):
        node.prev.next = node.next # current node's previous node points forward to the current's node next node
        node.next.prev = node.prev # current node's next node points back to the current's node previous node
    

    def put(self, key, value):
        if key in self.lookup:
            node = self.lookup[key]
            self._remove_node(node)
            node.value = value
            self._add_to_head(node)
        else:
            new_node = Node(key, value)
            if len(self.lookup) == self.capacity:
                evicted_node = self._pop_from_tail()
                del self.lookup[evicted_node.key]
            self._add_to_head(new_node)
            self.lookup[key] = new_node


    def get(self, key):
        if key not in self.lookup:
            return -1
        node = self.lookup[key]
        self._remove_node(node)
        self._add_to_head(node)
        return node.value

# Test Case 1: Basic operations
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
assert cache.get(1) == 1
cache.put(3, 3)  # Evicts key 2
assert cache.get(2) == -1
assert cache.get(3) == 3

# Test Case 2: Update existing key
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
cache.put(1, 10)  # Updates key 1, makes it most recent
assert cache.get(1) == 10
cache.put(3, 3)  # Evicts key 2 (1 is most recent)
assert cache.get(2) == -1
assert cache.get(1) == 10

# Test Case 3: Capacity 1
cache = LRUCache(1)
cache.put(1, 1)
cache.put(2, 2)  # Evicts 1
assert cache.get(1) == -1
assert cache.get(2) == 2
print("\n" + "=" * 60)
print("ALL TESTS PASSED! ✓")
print("=" * 60)