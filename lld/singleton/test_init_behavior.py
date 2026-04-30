"""
Demonstration: Understanding __init__ behavior in Singleton pattern
"""

from threading import Lock

# ========== Version 1: WITH __init__ and guard ==========
class SingletonWithInit:
    __instance = None
    _lock = Lock()

    def __new__(cls):
        if cls.__instance is None:
            with cls._lock:
                if cls.__instance is None:
                    cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        print(f"  __init__ called on instance {id(self)}")
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.value = 0
            print(f"  → Initialization logic executed (first time only)")
        else:
            print(f"  → Initialization skipped (already initialized)")


# ========== Version 2: WITHOUT __init__ ==========
class SingletonWithoutInit:
    __instance = None
    _lock = Lock()

    def __new__(cls):
        if cls.__instance is None:
            with cls._lock:
                if cls.__instance is None:
                    cls.__instance = super().__new__(cls)
        return cls.__instance

    # No __init__ method!


# ========== Version 3: WITH __init__ but NO guard ==========
class SingletonWithoutGuard:
    __instance = None
    _lock = Lock()

    def __new__(cls):
        if cls.__instance is None:
            with cls._lock:
                if cls.__instance is None:
                    cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        print(f"  __init__ called on instance {id(self)}")
        # NO guard - this will run EVERY time!
        self.value = 0
        print(f"  → Initialization logic executed (EVERY TIME!)")


print("=" * 70)
print("TEST 1: Singleton WITH __init__ and guard")
print("=" * 70)
s1 = SingletonWithInit()
s2 = SingletonWithInit()
s3 = SingletonWithInit()

print(f"\nInstance IDs:")
print(f"  s1: {id(s1)}")
print(f"  s2: {id(s2)}")
print(f"  s3: {id(s3)}")
print(f"  Same instance? {s1 is s2 is s3}")

print(f"\nValues:")
print(f"  s1.value: {s1.value}")
print(f"  s2.value: {s2.value}")
print(f"  s3.value: {s3.value}")


print("\n" + "=" * 70)
print("TEST 2: Singleton WITHOUT __init__")
print("=" * 70)
s4 = SingletonWithoutInit()
s5 = SingletonWithoutInit()
s6 = SingletonWithoutInit()

print(f"\nInstance IDs:")
print(f"  s4: {id(s4)}")
print(f"  s5: {id(s5)}")
print(f"  s6: {id(s6)}")
print(f"  Same instance? {s4 is s5 is s6}")

# Note: Python still calls object.__init__(), but it does nothing
print(f"\nNote: Python calls object.__init__() implicitly, but it does nothing")


print("\n" + "=" * 70)
print("TEST 3: Singleton WITH __init__ but NO guard (PROBLEMATIC!)")
print("=" * 70)
s7 = SingletonWithoutGuard()
s8 = SingletonWithoutGuard()
s9 = SingletonWithoutGuard()

print(f"\nInstance IDs:")
print(f"  s7: {id(s7)}")
print(f"  s8: {id(s8)}")
print(f"  s9: {id(s9)}")
print(f"  Same instance? {s7 is s8 is s9}")

print(f"\nValues (notice they're reset each time!):")
print(f"  s7.value: {s7.value}")
print(f"  s8.value: {s8.value}")
print(f"  s9.value: {s9.value}")

# Modify value
s7.value = 100
print(f"\nAfter setting s7.value = 100:")
print(f"  s7.value: {s7.value}")
print(f"  s8.value: {s8.value}")
print(f"  s9.value: {s9.value}")

# Create another instance - value gets reset!
s10 = SingletonWithoutGuard()
print(f"\nAfter creating s10:")
print(f"  s7.value: {s7.value}")  # Reset to 0!
print(f"  s10.value: {s10.value}")  # Also 0!


print("\n" + "=" * 70)
print("KEY INSIGHTS:")
print("=" * 70)
print("""
1. __init__ is called EVERY TIME you do Singleton(), but on the SAME instance
   - This is because __new__ always returns cls.__instance
   - Python automatically calls __init__ on whatever __new__ returns

2. If you REMOVE __init__:
   - Python still calls object.__init__() (parent class), which does nothing
   - The instance is STILL THE SAME (because __new__ controls that)
   - But you can't do initialization logic

3. If you have __init__ WITHOUT a guard:
   - Initialization logic runs EVERY TIME
   - This can reset instance variables!
   - This is usually NOT what you want

4. The guard (hasattr check) prevents re-initialization:
   - First call: Sets _initialized flag, runs init logic
   - Subsequent calls: Sees flag exists, skips init logic
   - Instance remains the same, but init only runs once
""")


