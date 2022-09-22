from numpy import empty, delete


class CircularQueue:
    def __init__(self, max_size, dtype):
        self.MAX_SIZE = max_size
        self.queue = empty(self.MAX_SIZE, dtype=dtype)
        self.front, self.rear = -1, -1

    def __iter__(self):
        return iter(self.queue)

    def is_full(self):
        return ((self.rear + 1) % self.MAX_SIZE) == self.front

    def is_empty(self):
        return self.front == -1

    def enqueue(self, data):
        if self.is_full():
            raise FullQueue

        if self.is_empty():
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.MAX_SIZE

        self.queue[self.rear] = data

    def dequeue(self):
        if self.is_empty():
            raise EmptyQueue

        temp = self.queue[self.front]
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.MAX_SIZE
        return temp


class EmptyQueue(Exception):
    """ Raised when a queue is empty"""


class FullQueue(Exception):
    """Raised when a queue is full"""
