from numpy import empty
from typing import TypeVar, Generic, Iterator

T = TypeVar("T")


class CircularQueue(Generic[T]):
    """
    Provides a circular queue that has a maximum size and provids the methods associated with a circular queue
    """

    def __init__(self, max_size: int, dtype: type[T]):
        self.max_size = max_size
        self.queue = empty(self.max_size, dtype=dtype)
        self.front, self.rear = -1, -1

    def __iter__(self) -> Iterator[T]:
        return iter(self.queue)

    def is_full(self) -> bool:
        """A method that returns True if the queue is full

        Returns:
            bool: Whether the queue is full or not
        """
        return ((self.rear + 1) % self.max_size) == self.front

    def is_empty(self) -> bool:
        """A method that returns True if the queue is empty

        Returns:
            bool: Whether the queue is empty or not
        """
        return self.front == -1

    def enqueue(self, data: T):
        """Adds an item to the end of the queue

        Args:
            data (T): The item to be added to the end of the queue

        Raises:
            FullQueue: If the queue is full then a FullQueue exception is raised
        """
        ###A: Queue Operation###

        if self.is_full():
            raise FullQueue

        if self.is_empty():
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.max_size

        self.queue[self.rear] = data

    def dequeue(self) -> T:
        """Removes the frontmost item from the queue and returns it

        Raises:
            EmptyQueue: If the queue is empty then an EmptyQueue exception is raised

        Returns:
            (T): The frontmost item in the queue
        """

        ###A: Queue Operation###

        if self.is_empty():
            raise EmptyQueue

        temp = self.queue[self.front]
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.max_size
        return temp


class EmptyQueue(Exception):
    """Raised when a queue is empty"""


class FullQueue(Exception):
    """Raised when a queue is full"""
