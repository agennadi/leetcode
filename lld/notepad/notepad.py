'''
Design a simple Notepad application (like Windows Notepad).

Requirements:

Open a file
Edit text
Save file
Undo / redo
Find text in document
Support multiple files/tabs

You do not need:
GUI
Syntax highlighting
Rich text formatting
'''
from abc import ABC, abstractmethod


class Document:
    def __init__(self, filename):
        self.filename = filename
        self.content = ''
        self.redo_stack = []
        self.undo_stack = []

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                self.content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.filename} not found")

    def insert(self, index, text):
        insert_command = InsertCommand(self, index, text)
        insert_command.execute()
        self.undo_stack.append(insert_command)

    def delete(self, index, length):
        delete_command = DeleteCommand(self, index, length)
        delete_command.execute()
        self.undo_stack.append(delete_command)

    def replace(self, index, text):
        replace_command = ReplaceCommand(self, index, text)
        replace_command.execute()
        self.undo_stack.append(replace_command)

    def undo(self):
        if self.undo_stack:
            action = self.undo_stack.pop()
            action.undo()
            self.redo_stack.append(action)
        else:
            return

    def redo(self):
        if self.redo_stack:
            action = self.redo_stack.pop()
            action.execute()
            self.undo_stack.append(action)
        else:
            return

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(self.content)
        self.undo_stack = []
        self.redo_stack = []


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class InsertCommand(Command):
    def __init__(self, document, index, text):
        self.document = document
        self.index = index
        self.text = text

    def execute(self):
        self.document.content = self.document.content[:self.index] + \
            self.text + self.document.content[self.index:]

    def undo(self):
        delete_command = DeleteCommand(
            self.document, self.index, len(self.text))
        delete_command.execute()


class DeleteCommand(Command):
    def __init__(self, document, index, length):
        self.document = document
        self.index = index
        self.length = length
        self.deleted_text = self.document.content[index: index+length]

    def execute(self):
        self.document.content = self.document.content[:self.index] + \
            self.document.content[self.index+self.length:]

    def undo(self):
        insert_command = InsertCommand(
            self.document, self.index, self.deleted_text)
        insert_command.execute()


class ReplaceCommand(Command):
    def __init__(self, document, index, text):
        self.document = document
        self.index = index
        self.text = text
        self.text_length = len(text)
        # Replace text of same length as new text
        self.replaced_text = self.document.content[index: index +
                                                   self.text_length]

    def execute(self):
        self.document.content = self.document.content[:self.index] + \
            self.text + self.document.content[self.index+self.text_length:]

    def undo(self):
        self.document.content = self.document.content[:self.index] + \
            self.replaced_text + \
            self.document.content[self.index+self.text_length:]


class Editor:
    def __init__(self):
        self.documents = dict()
        self.active = None

    def open_document(self, filename, load_file=False):
        if filename in self.documents:
            self.active = self.documents[filename]
            if load_file:
                self.active.load()
        else:
            self.create_document(filename)

    def switch_document(self, filename):
        if filename in self.documents:
            self.active = self.documents[filename]
        else:
            raise ValueError(f"Document {filename} not found")

    def create_document(self, filename):
        self.documents[filename] = Document(filename)
        self.active = self.documents[filename]

    def close_document(self):
        self.active = None

    def delete_document(self, filename):
        if filename in self.documents:
            if self.active == self.documents[filename]:
                self.active = None
            del self.documents[filename]
        else:
            raise ValueError(f"Document {filename} not found")

    def get_active_document(self):
        return self.active


# ==================== TEST CODE ====================

if __name__ == "__main__":
    print("=" * 60)
    print("NOTEPAD APPLICATION - TEST SUITE")
    print("=" * 60)

    # Test 1: Basic Insert
    print("\n--- Test 1: Basic Insert ---")
    doc = Document("test1.txt")
    doc.insert(0, "Hello")
    assert doc.content == "Hello", f"Expected 'Hello', got '{doc.content}'"
    print(f"✓ Insert 'Hello': {doc.content}")

    doc.insert(5, " World")
    assert doc.content == "Hello World", f"Expected 'Hello World', got '{doc.content}'"
    print(f"✓ Insert ' World': {doc.content}")

    # Test 2: Undo
    print("\n--- Test 2: Undo ---")
    doc.undo()
    assert doc.content == "Hello", f"Expected 'Hello', got '{doc.content}'"
    print(f"✓ Undo: {doc.content}")

    doc.undo()
    assert doc.content == "", f"Expected '', got '{doc.content}'"
    print(f"✓ Undo again: '{doc.content}'")

    # Test 3: Redo
    print("\n--- Test 3: Redo ---")
    doc.redo()
    assert doc.content == "Hello", f"Expected 'Hello', got '{doc.content}'"
    print(f"✓ Redo: {doc.content}")

    doc.redo()
    assert doc.content == "Hello World", f"Expected 'Hello World', got '{doc.content}'"
    print(f"✓ Redo again: {doc.content}")

    # Test 4: Delete
    print("\n--- Test 4: Delete ---")
    doc.delete(5, 6)
    assert doc.content == "Hello", f"Expected 'Hello', got '{doc.content}'"
    print(f"✓ Delete ' World': {doc.content}")

    doc.undo()
    assert doc.content == "Hello World", f"Expected 'Hello World', got '{doc.content}'"
    print(f"✓ Undo delete: {doc.content}")

    # Test 5: Replace
    print("\n--- Test 5: Replace ---")
    # Replace 6 chars starting at index 6 with "Python" (6 chars)
    doc.replace(6, "Python")
    assert doc.content == "Hello Python", f"Expected 'Hello Python', got '{doc.content}'"
    print(
        f"✓ Replace 'World' (6 chars) with 'Python' (6 chars): {doc.content}")

    doc.undo()
    assert doc.content == "Hello World", f"Expected 'Hello World', got '{doc.content}'"
    print(f"✓ Undo replace: {doc.content}")

    # Test 6: Multiple Operations
    print("\n--- Test 6: Multiple Operations ---")
    doc = Document("test2.txt")
    doc.insert(0, "A")
    doc.insert(1, "B")
    doc.insert(2, "C")
    assert doc.content == "ABC", f"Expected 'ABC', got '{doc.content}'"
    print(f"✓ Multiple inserts: {doc.content}")

    doc.undo()
    doc.undo()
    assert doc.content == "A", f"Expected 'A', got '{doc.content}'"
    print(f"✓ Two undos: {doc.content}")

    doc.redo()
    doc.redo()
    assert doc.content == "ABC", f"Expected 'ABC', got '{doc.content}'"
    print(f"✓ Two redos: {doc.content}")

    # Test 7: Editor - Multiple Documents
    print("\n--- Test 7: Editor - Multiple Documents ---")
    editor = Editor()
    editor.create_document("doc1.txt")
    doc1 = editor.get_active_document()
    doc1.insert(0, "Document 1")

    editor.create_document("doc2.txt")
    doc2 = editor.get_active_document()
    doc2.insert(0, "Document 2")

    assert doc1.content == "Document 1", f"Expected 'Document 1', got '{doc1.content}'"
    assert doc2.content == "Document 2", f"Expected 'Document 2', got '{doc2.content}'"
    print(f"✓ Document 1: {doc1.content}")
    print(f"✓ Document 2: {doc2.content}")

    # Test 8: Switch Documents
    print("\n--- Test 8: Switch Documents ---")
    editor.switch_document("doc1.txt")
    assert editor.get_active_document() == doc1, "Should switch to doc1"
    print(f"✓ Switched to doc1: {editor.get_active_document().content}")

    editor.switch_document("doc2.txt")
    assert editor.get_active_document() == doc2, "Should switch to doc2"
    print(f"✓ Switched to doc2: {editor.get_active_document().content}")

    # Test 9: Edge Cases
    print("\n--- Test 9: Edge Cases ---")
    doc = Document("test3.txt")

    # Undo when empty
    doc.undo()
    assert doc.content == "", "Undo on empty should do nothing"
    print("✓ Undo on empty stack: OK")

    # Redo when empty
    doc.redo()
    assert doc.content == "", "Redo on empty should do nothing"
    print("✓ Redo on empty stack: OK")

    # Insert at beginning
    doc.insert(0, "Start")
    doc.insert(0, "New")
    assert doc.content == "NewStart", f"Expected 'NewStart', got '{doc.content}'"
    print(f"✓ Insert at beginning: {doc.content}")

    # Test 10: Complex Sequence
    print("\n--- Test 10: Complex Sequence ---")
    doc = Document("test4.txt")
    doc.insert(0, "The quick brown")
    doc.insert(15, " fox")
    doc.insert(19, " jumps")
    assert doc.content == "The quick brown fox jumps", f"Expected 'The quick brown fox jumps', got '{doc.content}'"
    print(f"✓ Initial content: {doc.content}")

    doc.delete(4, 6)  # Delete "quick "
    assert doc.content == "The brown fox jumps", f"Expected 'The brown fox jumps', got '{doc.content}'"
    print(f"✓ After delete: {doc.content}")

    doc.undo()
    assert doc.content == "The quick brown fox jumps", f"Expected original, got '{doc.content}'"
    print(f"✓ Undo delete: {doc.content}")

    # Replace 3 chars starting at index 10 with "red" (3 chars)
    # Note: "brown" is 5 chars, but replace only replaces 3 (length of "red")
    doc.replace(10, "red")
    assert doc.content == "The quick redwn fox jumps", f"Expected 'The quick redwn fox jumps', got '{doc.content}'"
    print(f"✓ After replace: {doc.content}")

    doc.undo()
    assert doc.content == "The quick brown fox jumps", f"Expected original, got '{doc.content}'"
    print(f"✓ Undo replace: {doc.content}")

    # Test 11: Save clears stacks
    print("\n--- Test 11: Save clears undo/redo stacks ---")
    doc = Document("test5.txt")
    doc.insert(0, "Test")
    doc.undo()
    assert len(doc.undo_stack) == 0, "Undo stack should have one item"
    assert len(doc.redo_stack) == 1, "Redo stack should have one item"

    doc.save()
    assert len(doc.undo_stack) == 0, "Undo stack should be cleared after save"
    assert len(doc.redo_stack) == 0, "Redo stack should be cleared after save"
    print("✓ Save clears undo/redo stacks: OK")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED! ✓")
    print("=" * 60)
