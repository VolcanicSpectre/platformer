class Queue:
    def __init__(self, MAX_SIZE):
        self.MAX_SIZE = MAX_SIZE
        self.queue = []
        self.front, self.rear = -1, -1

    def is_full(self):
        return self.rear + 1 == self.MAX_SIZE

    def is_empty(self):
        return self.front == -1 and self.rear == -1

    def enqueue(self, item):
        if self.is_full():
            return
        if self.is_empty():
            self.front = 0
            self.rear = 0
        else:
            self.rear += 1
        self.queue[self.rear] = item

    def dequeue(self):
        if self.is_empty():
            return IndexError
        else:
            item = self.queue.pop(self.front)
            if self.front == 0 and self.rear == 0:
                self.front, self.rear = -1
            else:
                self.front += 1

            return item

class EmptyQueue(Exception):
    def __init__(self, message):
        pass