class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None


class Quence:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def push(self, value):
        node = Node(value)
        if self.head:
            self.tail.next = node
            self.tail = node
        else:
            self.head = node
            self.tail = node
        self.size += 1

    def poll(self):
        node = self.head
        if node.next:
            self.head = node.next
        else:
            self.head = self.tail = None
        self.size -= 1
        return node.value

    def peek(self):
        return self.head.value if self.head else None

    def is_empty(self):
        return False if self.size else True


def main(n):
    quence = Quence()
    print(f"quence has member: {not quence.is_empty()}")
    for i in range(n):
        quence.push(i)
    print(f"The size is {len(quence)}")
    print(f"quence has member: {not quence.is_empty()}")
    for i in range(quence.size):
        print(quence.peek())
        print(quence.poll())
    print(f"quence has member: {not quence.is_empty()}")


if __name__ == '__main__':
    main(15)
