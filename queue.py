class Queue:
    def __init__(self, max_size):
        self.MAX_SIZE = max_size
        self.queue = []
        self.front, self.rear = -1, -1

    def is_full(self):
        return self.rear + 1 == self.MAX_SIZE

    def is_empty(self):
        return self.front == -1 and self.rear == -1

    def enqueue(self, item):
        if self.is_full():
            return FullQueue
        if self.is_empty():
            self.front = 0
            self.rear = 0
        else:
            self.rear += 1
        self.queue[self.rear] = item

    def dequeue(self):
        if self.is_empty():
            return EmptyQueue
        else:
            item = self.queue.pop(self.front)
            if self.front == 0 and self.rear == 0:
                self.front, self.rear = -1
            else:
                self.front += 1

            return item


class EmptyQueue(Exception):
    """ Raised when a queue is empty"""
    pass


class FullQueue(Exception):
    """Raised when a queue is full"""
    pass
