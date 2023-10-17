from . import concepts, changes, env_types


class Queue:
    """
    A queue of change IDs to be processed
    """

    def __init__(self):
        self.values: list[changes.ChangeContext] = []

    def clear(self) -> None:
        self.values = []

    def add(self, id: concepts.ChangeId, replication: env_types.Replication) -> None:
        self.values.append(changes.ChangeContext(id=id, replication=replication))

    def pop(self) -> changes.ChangeContext:
        return self.values.pop()

    @property
    def empty(self) -> bool:
        return len(self.values) == 0

    def __repr__(self):
        return f'<Queue len={len(self.values)}>'
