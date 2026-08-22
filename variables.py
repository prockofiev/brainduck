from __future__ import annotations


class Variables:
    """Statically-allocated memory block in BrainDuck.

    A ``Variables`` instance represents a contiguous slice of Brainfuck
    memory (a number of binary cells). Instances are tracked in the class
    attribute ``memory`` so the compiler can resolve names and reclaim
    freed cells when a variable is deleted.

    Allocation uses first-fit: a new variable is placed into the earliest
    gap large enough to hold it, otherwise it is appended at the end.
    Deleting a variable frees its cells (used by later allocations) but
    intentionally does **not** clear the values stored there (documented
    behaviour of the ``del`` instruction).
    """

    memory: list[Variables] = []

    def __init__(self, name: str | None, size: int):
        if size <= 0:
            raise ValueError(f"Variable size must be positive, got {size!r}")

        self.name: str | None = name
        self.size: int = size

        if name is not None and Variables.get_by_name(name) is not None:
            raise ValueError(f"Variable {name!r} is already defined")

        self.index: int = 0
        for i in range(len(self.memory) - 1):
            start = self.memory[i].index + self.memory[i].size
            end = self.memory[i + 1].index
            if (end - start) >= size:
                self.index = start
                break
        else:
            if self.memory:
                self.index = self.memory[-1].index + self.memory[-1].size

        self.memory.append(self)
        self.memory.sort(key=lambda x: x.index)

    def remove(self) -> None:
        """Remove this variable from the memory registry."""
        if self in Variables.memory:
            Variables.memory.remove(self)

    @classmethod
    def get_by_name(cls, name: str) -> Variables | None:
        for variable in cls.memory:
            if variable.name == name:
                return variable
        return None

    def __str__(self) -> str:
        return f"Name: {self.name}    Size: {self.size}    Index: {self.index}"