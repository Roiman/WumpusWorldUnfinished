import itertools
from heapq import heappop, heappush


class PriorityQueue:
    def __init__(self):
        """
        Similar to the usual priority queue, but using
        (priority, -count) when pushing an entry, so newer
        entries are popped first.
        """
        self.pq = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.REMOVED = '<removed-task>'  # placeholder for a removed task
        self.counter = itertools.count()  # unique sequence count

    def push(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove(task)
        count = next(self.counter)
        # using -count so we have LIFO instead of FIFO
        entry = [(priority, -count), count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def remove(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    def __len__(self):
        return len(self.entry_finder)