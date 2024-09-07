# memory.py

class Memory:
    def __init__(self, max_items=5):
        self.memory = []
        self.max_items = max_items

    def add(self, item):
        self.memory.append(item)
        if len(self.memory) > self.max_items:
            self.memory.pop(0)

    def get_context(self):
        return "\n".join(self.memory)

    def clear(self):
        self.memory.clear()

    def get_last_n(self, n):
        return "\n".join(self.memory[-n:])

    def __len__(self):
        return len(self.memory)

    def __str__(self):
        return f"Memory(items={len(self)}, max_items={self.max_items})"