from jasonqwu_lib import *


class Node:
    def __init__(self, value=None):
        self._value = value
        self._next = None

    def get(self, attribute="next"):
        if attribute == "value":
            return self._value
        else:
            return self._next

    def set(self, content):
        self._next = content


class Stack:
    def __init__(self):
        self.head = None
        self.size = 0

    def push(self, value=None):
        node = Node(value)
        node.set(self.head)
        self.head = node
        self.size += 1

    def add(self, node):
        node.set(self.head)
        self.head = node
        self.size += 1

    def pop(self):
        res = None
        if self.head:
            node = self.head
            self.head = node.get()
            self.size -= 1
            res = node.get("value")
        return res

    def display(self):
        stack = Stack()
        for i in range(self.size):
            temp = self.pop()
            print(temp, end=' ')
            stack.push(temp)
        for i in range(stack.size):
            temp = stack.pop()
            self.push(temp)

    def is_empty(self):
        return self.size == 0

    def size(self):
        return self.size


class OrderStack(Stack):
    def push(self, value=None):
        node = Node(value)
        if self.head:
            if node.value > self.head.value:
                min = self.pop()
                self.push(node.value)
                self.add(Node(min))
            else:
                self.add(node)
        else:
            self.add(node)


class BackOrderStack(Stack):
    def push(self, value=None):
        node = Node(value)
        if self.head:
            if node.value < self.head.value:
                max = self.pop()
                self.push(node.value)
                self.add(Node(max))
            else:
                self.add(node)
        else:
            self.add(node)


class StackQueue():
    def __init__(self):
        self.a = Stack()
        self.b = Stack()

    def put(self, value):
        if not self.b.is_empty():
            for i in range(self.b.size):
                self.a.push(self.b.pop())
        self.a.push(value)

    def get(self):
        if self.b.is_empty():
            for i in range(self.a.size):
                self.b.push(self.a.pop())
        return self.b.pop()


def plaindrome(array):
    stack = Stack()
    result = Stack()
    for i in array:
        stack.push(i)
        result.push(i)
    for ign in range(len(array)):
        temp = stack.pop()
        result.push(temp)
    return result


def is_plaindrome(string):
    """
    >>> is_plaindrome("asdsa")
    True
    >>> is_plaindrome("asddsa")
    True
    >>> is_plaindrome("asdda")
    False
    """
    result = True
    length = len(string)
    mid = int(length / 2)
    stack = Stack()
    for i in range(mid):
        stack.push(string[i])
    drome = mid if length % 2 == 0 else mid + 1
    for i in range(drome, length):
        if string[i] == stack.pop():
            continue
        else:
            result = False
            break
    return result


def rev(stack):
    next_node = stack.head.next
    if next_node:
        node = Node(stack.pop())
        rev(stack)
        stack.push(node.value)


def ten_to_binary(n):
    if n > 1:
        stack = Stack()
        temp = n
        while temp > 0:
            stack.push(temp % 2)
            temp = temp // 2
        v = stack.pop()
        while not stack.is_empty():
            v = v * 10 + stack.pop()
        return v
    else:
        return n


def test_stack(n):
    stack = Stack()
    for i in range(n):
        print(i)
        stack.push(i)
    print(stack.is_empty())
    print("-----")
    for i in range(stack.size):
        print(stack.pop())
    print(stack.is_empty())
    print("-----")
    print(ten_to_binary(6))
    print(ten_to_binary(9))
    ostack = OrderStack()
    bstack = BackOrderStack()
    lst = [9, 6, 15, 4, 21, 7, 3, 34, 5, 18, 21, 17]
    for i in range(len(lst)):
        ostack.push(lst[i])
        bstack.push(lst[i])
    for i in range(ostack.size):
        print(ostack.pop())
    for i in range(bstack.size):
        print(bstack.pop())


def test_display(n):
    stack = Stack()
    for i in range(n):
        stack.push(i)
    stack.display()


def test_stackqueue(n):
    stack_queue = StackQueue()
    for i in range(n - 5):
        stack_queue.put(i)
    for i in range(n - 8):
        print(stack_queue.get())
    for i in range(n - 3, n):
        stack_queue.put(i)
    for i in range(n):
        print(stack_queue.get())


def test_rev(n):
    stack = Stack()
    for i in range(n):
        stack.push(i)
    rev(stack)
    for i in range(stack.size):
        print(stack.pop())


def main():
    str = input("请输入一个字符串：")
    print("Yes") if is_plaindrome(str) else print("No")

    # test_stack(19)
    # test_display(19)


if __name__ == '__main__':
    main()
