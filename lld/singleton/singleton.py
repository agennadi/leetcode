'''
 Singleton Pattern - Low Level Design Problem

## Problem Statement

Design and implement a **Singleton** class that ensures only one instance of the class can exist throughout the application lifecycle. The implementation should be thread-safe and handle edge cases properly.

---

## Functional Requirements

1. **Single Instance**: Only one instance of the class should exist
2. **Global Access**: Provide a way to access the singleton instance globally
3. **Lazy Initialization**: Instance should be created only when first requested (optional)
4. **Thread Safety**: Handle concurrent access in multi-threaded environments

---

## Example

```python
# First call - creates instance
instance1 = Singleton.get_instance()

# Subsequent calls - returns same instance
instance2 = Singleton.get_instance()

assert instance1 is instance2  # Same object
assert id(instance1) == id(instance2)  # Same memory address
```

---

## Design Constraints

1. **No Direct Instantiation**: Prevent creation via `Singleton()` constructor
2. **Thread Safety**: Use locks or other mechanisms for concurrent access
3. **Lazy vs Eager**: Choose appropriate initialization strategy
4. **Python-Specific**: Handle Python's module-level behavior

---

## Edge Cases to Handle

1. Multiple threads trying to create instance simultaneously
2. Subclassing the Singleton class
3. Serialization/deserialization (if applicable)
4. Reflection (if applicable)
5. Multiple imports of the same module

---

## Implementation Approaches to Consider

1. **Basic Singleton**: Simple class with class variable
2. **Thread-Safe Singleton**: Using locks
3. **Double-Checked Locking**: Optimized thread-safe approach
4. **Decorator Pattern**: Using decorator to make any class singleton
5. **Metaclass Approach**: Using metaclasses for singleton behavior

---

## Expected Deliverables

1. **Singleton class** with proper access control
2. **Thread-safe implementation**
3. **Test cases** demonstrating:
   - Single instance creation
   - Thread safety
   - Multiple access attempts
4. **Comparison** of different approaches (optional)

---

## Success Criteria

- ✅ Only one instance can be created
- ✅ Thread-safe for concurrent access
- ✅ Cannot be instantiated directly
- ✅ Global access point works correctly
- ✅ Clean, maintainable code

---

## Bonus (If Time Permits)

- Implement as a decorator (reusable for any class)
- Handle inheritance scenarios
- Compare performance of different approaches

---

**Time Limit**: ~30 minutes

'''
from threading import Lock


class BasicSingleton:
    __instance = None  # Class variable shared by all instance
    _lock = Lock()

    def __new__(cls):
        if cls.__instance is None:
            # first check
            with cls._lock:
                # second check to ensure that no other thread has created an instance
                if cls.__instance is None:
                    # parent's object class allocates memory and creates an **instance** of the class
                    cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        ''' 
        Skip __init__ if nothing needs to be initialized (e.g no instance variables needed). 
        If the logic is complex or if we want to prevent multiple initializations, we need to implement __init__. 
        '''
        if not hasattr(self, '_initialized'):
            self._initialized = True
            # do init logic here


def singleton(cls):
    instances = {}  # one instance per decorated class
    lock = Lock()

    def wrapper(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    # Preserve class attributes
    wrapper.__name__ = cls.__name__
    wrapper.__doc__ = cls.__doc__
    wrapper.__module__ = cls.__module__

    return wrapper


# ==================== TEST CODE ====================

if __name__ == "__main__":
    import threading
    import time

    print("=" * 60)
    print("SINGLETON PATTERN - TEST SUITE")
    print("=" * 60)

    # ========== BasicSingleton Tests ==========
    print("\n--- Test 1: BasicSingleton - Single Instance ---")
    instance1 = BasicSingleton()
    instance2 = BasicSingleton()
    instance3 = BasicSingleton()

    assert instance1 is instance2, "Instances should be the same"
    assert instance2 is instance3, "Instances should be the same"
    assert id(instance1) == id(instance2) == id(
        instance3), "All should have same memory address"
    print(f"✓ All instances are the same: {id(instance1)}")

    print("\n--- Test 2: BasicSingleton - Instance Variables ---")
    instance1.value = 42
    assert instance2.value == 42, "Instance variables should be shared"
    assert instance3.value == 42, "Instance variables should be shared"
    print("✓ Instance variables are shared across all references")

    print("\n--- Test 3: BasicSingleton - Initialization Guard ---")
    instance4 = BasicSingleton()
    assert hasattr(instance4, '_initialized'), "Should be initialized"
    assert instance4._initialized is True, "Initialization flag should be True"
    print("✓ Initialization guard works correctly")

    # ========== Decorator Tests ==========
    print("\n--- Test 4: Decorator - Single Instance ---")

    @singleton
    class Database:
        def __init__(self):
            self.connection = "connected"
            print("  Database initialized")

    db1 = Database()
    db2 = Database()
    db3 = Database()

    assert db1 is db2, "Database instances should be the same"
    assert db2 is db3, "Database instances should be the same"
    assert id(db1) == id(db2) == id(db3), "All should have same memory address"
    print(f"✓ All Database instances are the same: {id(db1)}")

    print("\n--- Test 5: Decorator - Multiple Classes ---")

    @singleton
    class Logger:
        def __init__(self):
            self.logs = []
            print("  Logger initialized")

        def log(self, message):
            self.logs.append(message)

        def get_logs(self):
            return self.logs

    @singleton
    class Config:
        def __init__(self):
            self.settings = {}
            print("  Config initialized")

    logger1 = Logger()
    logger2 = Logger()
    config1 = Config()
    config2 = Config()

    assert logger1 is logger2, "Logger instances should be the same"
    assert config1 is config2, "Config instances should be the same"
    assert logger1 is not config1, "Different classes should have different instances"
    print("✓ Different classes maintain separate singleton instances")

    print("\n--- Test 6: Decorator - Instance Variables ---")
    logger1.log("First log")
    logger2.log("Second log")
    assert len(logger1.get_logs()) == 2, "Logs should be shared"
    assert len(logger2.get_logs()) == 2, "Logs should be shared"
    print(f"✓ Logs shared: {logger1.get_logs()}")

    print("\n--- Test 7: Decorator - Parameters (First Call Wins) ---")

    @singleton
    class Settings:
        def __init__(self, name="default"):
            self.name = name
            print(f"  Settings initialized with name: {name}")

    settings1 = Settings("production")
    settings2 = Settings("development")  # This call's args are ignored

    assert settings1 is settings2, "Instances should be the same"
    assert settings1.name == "production", "First call's parameters should be used"
    assert settings2.name == "production", "Should use first call's parameters"
    print("✓ First call's parameters are used (subsequent calls ignored)")

    # ========== Thread Safety Tests ==========
    print("\n--- Test 8: BasicSingleton - Thread Safety ---")
    instances = []
    lock = threading.Lock()

    def create_instance():
        instance = BasicSingleton()
        with lock:
            instances.append(instance)

    threads = []
    for _ in range(10):
        t = threading.Thread(target=create_instance)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # All instances should be the same
    first_instance = instances[0]
    for instance in instances:
        assert instance is first_instance, "All thread instances should be the same"

    assert len(set(id(inst) for inst in instances)
               ) == 1, "Only one unique instance should exist"
    print(
        f"✓ Thread safety: {len(instances)} threads created, all using same instance: {id(first_instance)}")

    print("\n--- Test 9: Decorator - Thread Safety ---")
    decorator_instances = []

    @singleton
    class ThreadSafeClass:
        def __init__(self):
            self.created_at = time.time()

    def create_decorator_instance():
        instance = ThreadSafeClass()
        with lock:
            decorator_instances.append(instance)

    threads = []
    for _ in range(10):
        t = threading.Thread(target=create_decorator_instance)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # All instances should be the same
    first_decorator_instance = decorator_instances[0]
    for instance in decorator_instances:
        assert instance is first_decorator_instance, "All thread instances should be the same"

    assert len(set(id(inst) for inst in decorator_instances)
               ) == 1, "Only one unique instance should exist"
    print(
        f"✓ Thread safety: {len(decorator_instances)} threads created, all using same instance: {id(first_decorator_instance)}")

    # ========== Edge Cases ==========
    print("\n--- Test 10: Edge Cases - Multiple Instantiations ---")
    singleton1 = BasicSingleton()
    singleton2 = BasicSingleton()
    singleton3 = BasicSingleton()

    # Modify one
    singleton1.test_value = "modified"

    # All should reflect the change
    assert singleton2.test_value == "modified"
    assert singleton3.test_value == "modified"
    print("✓ Changes to one reference affect all references")

    print("\n--- Test 11: Edge Cases - Decorator with Different Args ---")

    @singleton
    class TestClass:
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

    obj1 = TestClass(1, 2)
    obj2 = TestClass(3, 4)  # Args ignored

    assert obj1 is obj2, "Should be same instance"
    assert obj1.x == 1 and obj1.y == 2, "Should use first call's args"
    assert obj2.x == 1 and obj2.y == 2, "Should use first call's args"
    print("✓ Decorator correctly ignores subsequent initialization args")

    print("\n--- Test 12: Edge Cases - Class Attributes Preserved ---")

    @singleton
    class DocumentedClass:
        """This is a test class."""
        class_var = "test"

    assert DocumentedClass.__name__ == "DocumentedClass", "Class name should be preserved"
    assert DocumentedClass.__doc__ == "This is a test class.", "Docstring should be preserved"
    print("✓ Class attributes (name, docstring) are preserved")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED! ✓")
    print("=" * 60)
