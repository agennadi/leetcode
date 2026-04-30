# State Pattern - Quick Cheat Sheet

## 🎯 Core Concept
**Objects change behavior when their internal state changes.**

---

## 📐 Structure

```python
# 1. Abstract State (interface)
class State(ABC):
    def __init__(self):
        self.context = None  # Reference to context
    
    @abstractmethod
    def action1(self): pass
    @abstractmethod
    def action2(self): pass

# 2. Concrete States (implementations)
class ConcreteStateA(State):
    def action1(self):
        # Do something
        self.context.change_state(ConcreteStateB())  # ✅ Change state
    
    def action2(self):
        # State-specific behavior
        pass

# 3. Context (manages states)
class Context:
    def __init__(self):
        self.state = ConcreteStateA()
        self.state.context = self
    
    def change_state(self, new_state):
        self.state = new_state  # ✅ ONLY place states change
        self.state.context = self
    
    def action1(self):
        self.state.action1()  # Delegate to state
```

---

## ✅ DO's

1. **States change via context:**
   ```python
   self.context.change_state(NewState())
   ```

2. **Context delegates to state:**
   ```python
   def action(self):
       self.state.action()  # Delegate
   ```

3. **Store context reference in state:**
   ```python
   class State:
       def __init__(self):
           self.context = None  # Set by context
   ```

4. **Single point of state change:**
   ```python
   def change_state(self, new_state):
       self.state = new_state  # Only here!
   ```

---

## ❌ DON'Ts

1. **States changing themselves directly:**
   ```python
   self.context.state = NewState()  # ❌ WRONG
   ```

2. **Context changing state directly:**
   ```python
   def action(self):
       self.state = NewState()  # ❌ Use change_state()
   ```

3. **Generic handle_input() method:**
   ```python
   def handle_input(self, input):  # ❌ Too generic
   ```

---

## 🔄 State Transition Flow

```
State A → (action) → State B
  ↑                      ↓
  └────── (action) ──────┘
```

**Example:**
```
Idle → select_code() → WaitingForPayment
WaitingForPayment → insert_money() → Dispensing
Dispensing → dispense() → Idle
```

---

## 📋 Checklist

- [ ] Abstract state defines interface (all actions)
- [ ] Each concrete state implements all abstract methods
- [ ] Context has `change_state()` method (single point of change)
- [ ] States call `context.change_state()` to transition
- [ ] Context delegates actions to current state
- [ ] States have reference to context (`self.context`)

---

## 🎨 Template

```python
from abc import ABC, abstractmethod

# 1. Abstract State
class State(ABC):
    def __init__(self):
        self.context = None
    
    @abstractmethod
    def action(self): pass

# 2. Concrete States
class StateA(State):
    def action(self):
        if condition:
            self.context.change_state(StateB())

class StateB(State):
    def action(self):
        self.context.change_state(StateA())

# 3. Context
class Context:
    def __init__(self):
        self.state = StateA()
        self.state.context = self
    
    def change_state(self, new_state):
        self.state = new_state
        self.state.context = self
    
    def action(self):
        self.state.action()
```

---

## 🔑 Key Takeaway

**States decide WHEN to change, Context decides HOW to change.**

States: `"I want to change to StateB"`
Context: `"Okay, I'll change the state and set up the reference"`

---

## 💡 Remember

1. **One state at a time** - Context has single `self.state`
2. **States are stateless** - They don't store data (context does)
3. **Context is stateful** - Stores data and current state
4. **Delegation pattern** - Context delegates to state

