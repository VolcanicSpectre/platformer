from numpy import empty, delete
from render_object import RenderObject


class Queue:
    def __init__(self, max_size, dtype):
        self.MAX_SIZE = max_size
        self.queue = empty(self.MAX_SIZE, dtype=dtype)
        self.front, self.rear = -1, -1

    def __iter__(self):
        return iter(self.queue)

    def is_full(self):
        return self.rear + 1 == self.MAX_SIZE

    def is_empty(self):
        return self.front == -1 and self.rear == -1

    def enqueue(self, item):
        if self.is_full():
            raise FullQueue
        if self.is_empty():
            self.front = 0
            self.rear = 0
        else:
            self.rear += 1
        self.queue[self.rear] = item

    def dequeue(self):
        if self.is_empty():
            raise EmptyQueue
        else:
            item = self.queue[self.front]
            self.queue = delete(self.queue, self.front)
            if self.front == 0 and self.rear == 0:
                self.front, self.rear = -1
            else:
                self.front += 1

            return item


class CircularQueue(Queue):
    def __init__(self, max_size, dtype):
        Queue.__init__(self, max_size, dtype)

    def is_full(self):
        return ((self.rear + 1) % self.MAX_SIZE) == self.front

    def enqueue(self, item):
        if self.is_full():
            raise FullQueue

        if self.is_empty():
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.MAX_SIZE

        self.queue[self.rear] = item

    def dequeue(self):
        if self.is_empty():
            raise EmptyQueue
        else:
            item = self.queue[self.front]
            self.queue = delete(self.queue, self.front)
            if self.front == 0 and self.rear == 0:
                self.front = -1
                self.rear = -1
            else:
                self.front = (self.front + 1) % self.MAX_SIZE

            return item


class EmptyQueue(Exception):
    """ Raised when a queue is empty"""
    pass


class FullQueue(Exception):
    """Raised when a queue is full"""
