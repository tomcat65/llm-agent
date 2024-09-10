# memory.py

from typing import List

class Memory:
    def __init__(self, max_items: int = 5):
        self.memory: List[str] = []
        self.max_items = max_items

    def add(self, item: str) -> None:
        self.memory.append(item)
        if len(self.memory) > self.max_items:
            self.memory.pop(0)

    def get_context(self) -> str:
        return "\n".join(self.memory)

    def clear(self) -> None:
        self.memory.clear()

    def get_last_n(self, n: int) -> str:
        return "\n".join(self.memory[-n:])

    def __len__(self) -> int:
        return len(self.memory)

    def __str__(self) -> str:
        return f"Memory(items={len(self)}, max_items={self.max_items})"

    def status(self) -> str:
        return f"Memory status: {len(self)}/{self.max_items} items stored\nContents:\n" + "\n".join(f"{i+1}. {item[:50]}..." for i, item in enumerate(self.memory))