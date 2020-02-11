class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value}"


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self):
        arr = []
        current = self.head
        while current:
            arr.append(current.value)
            current = current.next
        return f"Queue: {arr}"

    def __repr__(self):
        arr = []
        current = self.head
        while current:
            arr.append(current.value)
            current = current.next
        return f"Queue: {arr}"

    def len(self):
        return self.size

    def enqueue(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        if not self.head:
            return None
        else:
            old_val = self.head.value
            self.head = self.head.next
            self.size -= 1
            return old_val