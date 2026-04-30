'''
Notepad with Cursor Movement - Low Level Design Problem

## Problem Statement

Design and implement a **Notepad** text editor that supports cursor movement operations (up, down, left, right, page up, page down) and efficient text representation. This is a **data structure design challenge** focused on how text editors internally represent text and manage cursor positions.

---

## Functional Requirements

### 1. Cursor Movement Operations

- **Left**: Move cursor one character to the left
- **Right**: Move cursor one character to the right
- **Up**: Move cursor one line up (same column position if possible)
- **Down**: Move cursor one line down (same column position if possible)
- **Page Up**: Move cursor up by one page (e.g., 20 lines)
- **Page Down**: Move cursor down by one page (e.g., 20 lines)

### 2. Cursor Position

- Track current cursor position: (row, column)
- Cursor position should be valid (within text bounds)
- When moving up/down, maintain column position if possible, otherwise move to end of line

### 3. Text Representation

- Efficiently represent text with line breaks
- Support getting text at cursor position
- Support getting current line content

### 4. Basic Text Operations (Optional - for context)

- Insert text at cursor position
- Delete character at cursor position
- Not required for core problem, but useful for understanding the data structure

---

## Example

```python
notepad = Notepad()
notepad.insert_text("Hello\nWorld\nPython")
# Text content:
# Line 0: "Hello"
# Line 1: "World"
# Line 2: "Python"
# Cursor: (0, 0) - at start of "Hello"

# Move right
notepad.move_right()  # Cursor: (0, 1)
notepad.move_right()  # Cursor: (0, 2)

# Move down
notepad.move_down()   # Cursor: (1, 2) - same column in "World"
notepad.move_left()   # Cursor: (1, 1)

# Move up
notepad.move_up()     # Cursor: (0, 1) - back to "Hello"

# Page operations
notepad.page_down()  # Move down by page size (e.g., 20 lines)
notepad.page_up()    # Move up by page size
```

---

## Design Constraints

1. **Data Structure Focus**: Choose efficient data structure for text representation
   - Options: List of strings (lines), Linked list of lines, Rope data structure
   - Consider: Insertion/deletion efficiency, cursor movement efficiency
   
2. **Cursor Tracking**: Efficiently track cursor position (row, column)

3. **Performance**: Cursor movement operations should be O(1) or O(log n) where possible

4. **Memory**: Efficient memory usage for large text files

5. **No Built-in Libraries**: Don't use specialized text editor libraries

---

## Expected Data Structures

### Option 1: List of Lines (Simple)
```python
text = ["Hello", "World", "Python"]  # List of strings
cursor = (row=0, col=0)  # (line_index, char_index)
```

**Pros:**
- Simple to implement
- Easy to understand
- O(1) access to line

**Cons:**
- O(n) for insertion/deletion in middle of line
- O(n) for moving cursor left/right within line

### Option 2: Linked List of Lines (Better for large files)
```python
class LineNode:
    content: str
    next: LineNode
    prev: LineNode
```

**Pros:**
- O(1) insertion/deletion of lines
- Efficient for large files

**Cons:**
- More complex implementation
- Still O(n) for moving within line

### Option 3: Rope Data Structure (Advanced)
- Binary tree of string fragments
- More complex but very efficient for large texts

**Recommendation**: Start with **List of Lines** for simplicity, then discuss optimizations.

---

## Expected Classes

1. **Notepad**:
   - Attributes: `text_lines` (list of strings), `cursor_row`, `cursor_col`, `page_size`
   - Methods: `move_left()`, `move_right()`, `move_up()`, `move_down()`, 
             `page_up()`, `page_down()`, `get_cursor_position()`, 
             `get_current_line()`, `get_text()`

2. **Optional Helper Classes**:
   - `Cursor` class (optional) to encapsulate cursor position
   - `Line` class (optional) for more complex line representation

---

## Edge Cases to Handle

1. **Cursor at Boundaries**:
   - Moving left at start of line (0, 0)
   - Moving right at end of line
   - Moving up at first line
   - Moving down at last line

2. **Uneven Line Lengths**:
   - Moving up/down when target line is shorter
   - Example: Line 0 has 10 chars, Line 1 has 5 chars
   - Cursor at (0, 8) → move down → should go to (1, 5) not (1, 8)

3. **Empty Text**:
   - Cursor movement when text is empty

4. **Page Operations**:
   - Page up at beginning of text
   - Page down at end of text

5. **Single Line Text**:
   - Moving up/down when there's only one line

---
'''


class LineNode:
    """Represents a single line in the notepad using doubly linked list"""

    def __init__(self, content=""):
        self.content = content  # String content of the line
        self.next = None  # Next line node
        self.prev = None  # Previous line node


class Notepad:
    def __init__(self):
        self.head = None  # First line node
        self.tail = None  # Last line node
        self.current_line = None  # Current line node (cursor is on this line)
        self.cursor_col = 0  # Column position within current line
        self.page_size = 20  # Number of lines per page

    def insert_text(self, text):
        """Insert text into notepad. Split by newlines to create multiple lines."""
        if not text:
            # Empty text - create one empty line
            if self.head is None:
                new_line = LineNode("")
                self.head = new_line
                self.tail = new_line
                self.current_line = new_line
                self.cursor_col = 0
            return

        lines = text.split('\n')

        for i, line_content in enumerate(lines):
            new_line = LineNode(line_content)

            if self.head is None:
                # First line
                self.head = new_line
                self.tail = new_line
            else:
                # Append to tail
                self.tail.next = new_line
                new_line.prev = self.tail
                self.tail = new_line

        # After inserting all text, move cursor to start of first line
        if self.head:
            self.current_line = self.head
            self.cursor_col = 0

    def get_cursor_position(self):
        """Get current cursor position as (row, column)"""
        if self.current_line is None:
            return (0, 0)

        # Count row number by traversing from head
        row = 0
        node = self.head
        while node and node != self.current_line:
            row += 1
            node = node.next

        return (row, self.cursor_col)

    def set_cursor(self, row, col):
        """Set cursor to specific position (for testing)"""
        # Find line at row
        node = self.head
        for _ in range(row):
            if node is None:
                return
            node = node.next

        if node:
            self.current_line = node
            # Clamp column to line length
            self.cursor_col = min(col, len(node.content))

    def get_current_line(self):
        """Get content of current line"""
        if self.current_line is None:
            return ""
        return self.current_line.content

    def get_text(self):
        """Get all text content"""
        if self.head is None:
            return ""

        lines = []
        node = self.head
        while node:
            lines.append(node.content)
            node = node.next

        return '\n'.join(lines)

    def move_left(self):
        """Move cursor one character to the left"""
        if self.current_line is None:
            return

        if self.cursor_col > 0:
            # Move within current line
            self.cursor_col -= 1
        elif self.current_line.prev:
            # At start of line, move to end of previous line
            self.current_line = self.current_line.prev
            self.cursor_col = len(self.current_line.content)

    def move_right(self):
        """Move cursor one character to the right"""
        if self.current_line is None:
            return

        line_length = len(self.current_line.content)

        if self.cursor_col < line_length:
            # Move within current line
            self.cursor_col += 1
        elif self.current_line.next:
            # At end of line, move to start of next line
            self.current_line = self.current_line.next
            self.cursor_col = 0

    def move_up(self):
        """Move cursor one line up (maintain column if possible)"""
        if self.current_line is None or self.current_line.prev is None:
            return

        self.current_line = self.current_line.prev
        # Maintain column position, but clamp to line length
        line_length = len(self.current_line.content)
        self.cursor_col = min(self.cursor_col, line_length)

    def move_down(self):
        """Move cursor one line down (maintain column if possible)"""
        if self.current_line is None or self.current_line.next is None:
            return

        self.current_line = self.current_line.next
        # Maintain column position, but clamp to line length
        line_length = len(self.current_line.content)
        self.cursor_col = min(self.cursor_col, line_length)

    def page_up(self):
        """Move cursor up by page_size lines"""
        if self.current_line is None:
            return

        # Move up by page_size lines
        for _ in range(self.page_size):
            if self.current_line.prev is None:
                break
            self.current_line = self.current_line.prev

        # Maintain column position, but clamp to line length
        line_length = len(self.current_line.content)
        self.cursor_col = min(self.cursor_col, line_length)

    def page_down(self):
        """Move cursor down by page_size lines"""
        if self.current_line is None:
            return

        # Move down by page_size lines
        for _ in range(self.page_size):
            if self.current_line.next is None:
                break
            self.current_line = self.current_line.next

        # Maintain column position, but clamp to line length
        line_length = len(self.current_line.content)
        self.cursor_col = min(self.cursor_col, line_length)


# Test Case 1: Basic cursor movement
notepad = Notepad()
notepad.insert_text("Hello\nWorld")
assert notepad.get_cursor_position() == (0, 0)
notepad.move_right()  # (0, 1)
notepad.move_right()  # (0, 2)
notepad.move_down()   # (1, 2) - same column in "World"
assert notepad.get_cursor_position() == (1, 2)

# Test Case 2: Moving up/down with different line lengths
notepad = Notepad()
notepad.insert_text("Long line here\nShort")
notepad.set_cursor(0, 12)  # At position 12 in "Long line here"
assert notepad.get_cursor_position() == (0, 12)
notepad.move_down()
# Should go to end of "Short", not (1, 12)
assert notepad.get_cursor_position() == (1, 5)

# Test Case 3: Boundary conditions
notepad = Notepad()
notepad.insert_text("Hello")
notepad.set_cursor(0, 0)
assert notepad.get_cursor_position() == (0, 0)
notepad.move_left()  # Should stay at (0, 0)
assert notepad.get_cursor_position() == (0, 0)
notepad.move_right()  # Should move to (0, 1)
assert notepad.get_cursor_position() == (0, 1)
notepad.set_cursor(0, 5)  # At end
assert notepad.get_cursor_position() == (0, 5)
notepad.move_right()  # Should stay at (0, 5)
assert notepad.get_cursor_position() == (0, 5)

# Test Case 4: Page operations
notepad = Notepad()
# Insert 50 lines of text (all at once)
all_lines = '\n'.join([f"Line {i}" for i in range(50)])
notepad.insert_text(all_lines)
notepad.set_cursor(25, 0)
assert notepad.get_cursor_position() == (25, 0)
notepad.page_up()  # Should move to around line 5 (if page_size=20)
assert notepad.get_cursor_position() == (5, 0)
notepad.page_down()  # Should move to around line 25
assert notepad.get_cursor_position() == (25, 0)

print("All test cases passed! ✅")
