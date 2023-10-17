from __future__ import absolute_import
import pysnooper
import stack_lib
import pytest
from jasonqwu_lib import *


@Decorator.add_str
class Node:
    '''静态变量'''
    '''声明一下静态属性'''
    _counter = 0
    __slots__ = ["_value", "_next"]

    def __init__(self, value=None):
        if value is None:
            self._value = None
        else:
            self._value = value
            Node._counter += 1
        self._next = None

    def __iter__(self):
        node = self
        while node is not None:
            yield node
            node = node._next

    def __str__(self):
        return str(self._value)

    def __eq__(self, node):
        self._value = node._value
        self._next = node._next

    def is_none(self):
        if self.value is None:
            return True
        else:
            return False

    @property
    def counter(self):
        return self._counter

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @value.deleter
    def value(self):
        self._value = None

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node):
        self._next = node

    @next.deleter
    def next(self):
        self._next = None


class BidirectionalNode(Node):
    __slots__ = ["_value", "_last", "_next"]

    def __init__(self, _value=None):
        super().__init__(_value)
        self._last = None

    @property
    def last(self):
        return self._last

    @last.setter
    def last(self, node):
        self._last = node

    @last.deleter
    def last(self):
        self._last = None


class List:
    __slots__ = ["_head", "_length"]

    def __init__(self, lst=None):
        self._length = 0
        if lst is None or lst == []:
            self._head = Node()
            return
        else:
            self._head = Node(lst[0])
            self._length = 1
        pointer = self.head
        for i in range(1, len(lst)):
            temp = Node(lst[i])
            # debug(f"temp.counter = {temp.counter}", )
            self._length += 1
            pointer.next = temp
            pointer = temp

    def __getitem__(self, index):
        if self.head.value is None:
            return
        index = Tool.adjust(index, self.length)

        node = self.head
        if index > 0:
            for ign in range(index):
                node = node.next
            return node.value
        else:
            return None

    def __setitem__(self, index, value):
        if self.head.value is None:
            return
        index = Tool.adjust(index, self.length)

        node = self.head
        if index > 0:
            for ign in range(index):
                node = node.next
            node.value = value
        else:
            return None

    def __len__(self):
        if self.head is None:
            return 0
        return self.length

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, node):
        self._head = node

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        self._length = length

    def is_none(self):
        if self.length == 0:
            return True
        else:
            return False

    def append(self, node=None):
        if node.is_none():
            return
        if self.is_none():
            self.head = node
        else:
            p = self.head
            while p.next is not None:
                p = p.next
            p.next = node
        self._length += 1

    def insert(self, index, node):
        if index >= self.length:
            self.append(node)
            return
        index = Tool.adjust(index, self.length)

        if index > 0:
            p = self.head
            for ign in range(index - 1):
                p = p.next
            node.next = p.next
            p.next = node
        else:
            node.next = self.head
            self.head = node
        self._length += 1

    def insert_by_sort(self, node, order=True):
        self.back()
        # 先找到头节点
        pointer = self._head
        if pointer is not None:
            if order:
                # 从头向尾，找到 _value 比节点数大的地方
                while pointer is not None and node._value < pointer._value:
                    pre_pointer = pointer
                    pointer = pointer._next
            else:
                # 从头向尾，找到 _value 比节点数小的地方
                while pointer is not None and node._value > pointer._value:
                    pre_pointer = pointer
                    pointer = pointer._next
            if pointer is not None:
                # 从中间插入
                if pointer != self._head:
                    pre_pointer._next = node
                    node._next = pointer
                # 从头部插入
                else:
                    node._next = self._head
                    self._head = node
            # 从尾部追加
            else:
                pre_pointer._next = node
        # 插入空列表
        else:
            self._head = node
        self._length += 1
        self.back()

    def pop(self, index=0):
        index = Tool.adjust(index, self.length)

        if index > 0:
            p = self.head
            for ign in range(index - 1):
                p = p.next
            node = p.next
            p.next = node.next
        else:
            node = self.head
            self.head = node.next
        self._length -= 1
        return node

    # @pysnooper.snoop(watch=("_start"))
    def back(self, start=0, end=-1):
        # debug("_length = {}".format(self._length))
        if end < 0 or end >= self._length:
            end = self._length - 1
        elif start >= self._length - 1 or end <= start or end == 0:
            return
        _head = self._head
        _prev = None
        _curr = self._head
        if _curr is None:
            return
        i = 0
        if start > 0:
            while i < start:
                _prev = _curr
                _curr = _curr._next
                i += 1
            _start = _prev
            _end = _curr
        else:
            i = -1
        while i <= end and _curr is not None:
            _next = _curr._next
            _curr._next = _prev
            _prev = _curr
            _curr = _next
            i += 1
        if start > 0:
            _start._next = _prev
            _end._next = _curr
        else:
            _head = _prev
        self._head = _head

    # @pysnooper.snoop(watch=("node"))
    def _recursion(self, node, tail, _length):
        if _length <= 0:
            tail = node._next
            return node, tail
        if node is None or node._next is None:
            tail = None
            return node, tail
        _length -= 1
        _head, tail = self._recursion(node._next, tail, _length)
        node._next._next = node
        node._next = None
        return _head, tail

    # @pysnooper.snoop(watch=("start", "end", "_prev", "_tail"))
    def reversed(self, start=0, end=-1):
        if end < 0 or end >= self._length:
            end = self._length - 1
        elif start >= self._length - 1 or end <= start or end == 0:
            return
        _head = self._head
        _prev = None
        _curr = self._head
        _tail = None
        i = 0
        if start > 0:
            while i < start:
                _prev = _curr
                _curr = _curr._next
                i += 1
            _start = _curr
        else:
            i = -1
            _start = self._head
        _curr, _tail = self._recursion(_start, _tail, end - start)
        if start > 0:
            _prev._next._next = _tail
            _prev._next = _curr
        else:
            _head = _curr
        self._head = _head

    def print(self, show=True):
        result = []
        if self.head.value is None \
           or self.head.value == []:
            return result
        for node in self.head:
            result.append(node.value)
        if show:
            debug(f"result = {result}")
        return result


class TestList:
    @pytest.mark.order(2)
    @pytest.mark.parametrize("nums", [[2, 3, 5, 8, 9, 10, 18, 26, 32], []])
    def test_print(self, nums):
        lst = List(nums)
        assert lst.print(False) == nums

    @pytest.mark.order(1)
    @pytest.mark.parametrize("nums", [[2, 3, 5, 8, 9, 10, 18, 26, 32], []])
    def test_len(self, nums):
        lst = List(nums)
        assert len(lst) == len(nums)

    @pytest.mark.parametrize("nums, item",
                             [([2, 3, 5, 8, 9, 10, 18, 26, 32], 6),
                              ([], 4)])
    def test_append(self, nums, item):
        lst = List(nums)
        lst.append(Node(item))
        nums.append(item)
        assert lst.print(False) == nums

    @pytest.mark.parametrize("nums, index, item",
                             [([2, 3, 5, 8, 9, 10, 18, 26, 32], 3, 6),
                              ([2, 3, 5, 8, 9, 10, 18, 26, 32], -3, 6),
                              ([2, 3, 5, 8, 9, 10, 18, 26, 32], -18, 6),
                              ([], 8, 4)])
    def test_insert(self, nums, index, item):
        lst = List(nums)
        lst.insert(index, Node(item))
        nums.insert(index, item)
        assert lst.print(False) == nums

    @pytest.mark.order(index=2, before="test_print")
    @pytest.mark.parametrize("nums, index",
                             [([2, 3, 5, 8, 9, 10, 18, 26, 32], 5),
                              ([], 3)])
    def test_get(self, nums, index):
        lst = List(nums)
        if nums is None or nums == []:
            assert lst[index] is None
        else:
            assert lst[index] == nums[index]

    @pytest.mark.parametrize("nums, item, index",
                             [([2, 3, 5, 8, 9, 10, 18, 26, 32], 99, 5),
                              ([], 55, 3)])
    def test_set(self, nums, item, index):
        lst = List(nums)
        lst[index] = item
        if nums is None or nums == []:
            assert lst[index] is None
        else:
            nums[index] = item
            assert lst.print(False) == nums

    @pytest.mark.parametrize("nums, index",
                             [([2, 3, 5, 8, 9, 10, 18, 26, 32], 5),
                              ([], 3)])
    def test_pop(self, nums, index):
        lst = List(nums)
        if nums is None or nums == []:
            assert lst.is_none()
        else:
            lst.pop(index)
            nums.pop(index)
            assert lst.print(False) == nums


class ImitateList(List):
    def __init__(self, value=None):
        super().__slots__.append(["_value", "_next"])
        self._length = 0
        if value is None:
            self._head = 0
            self._value = None
            self._next = None
            return
        if value == []:
            self._head = 0
            self._value = []
            self._next = []
            return
        self._head = 1
        self._value = [value[i] for i in range(len(value))]
        self._next = []
        for i in range(len(value) - 1):
            self.all_next.append(i + 2)
            self._length += 1
        self.all_next.append(0)
        self._length += 1

    def __getitem__(self, index):
        index = Tool.adjust(index, self.length)

        if index > 0:
            for i in range(self.length):
                if self._next[i] == index:
                    return self._value[self._next[i]]
        else:
            return None

    def __setitem__(self, index, item):
        index = Tool.adjust(index, self.length)

        if index > 0:
            for i in range(self.length):
                if self._next[i] == index:
                    self._value[self._next[i]] = item
        else:
            return None

    @property
    def all_value(self):
        if self._value is None:
            return None
        elif self._value == []:
            return []
        else:
            return self._value

    @all_value.setter
    def all_value(self, value):
        self._value = value

    def get_value(self, index):
        if self._value is None:
            return None
        elif self._value == []:
            return []
        else:
            return self._value[index]

    def set_value(self, index, value):
        index = Tool.adjust(index, self.length)
        if self._value is None:
            return None
        elif self._value == []:
            return []
        else:
            self._value[index] = value

    @property
    def all_next(self):
        return self._next

    @all_next.setter
    def all_next(self, next):
        self._next = next

    def get_next(self, index):
        if self._next is None:
            return None
        elif self._next == []:
            return []
        else:
            return self._next[index]

    def set_next(self, index, next):
        index = Tool.adjust(index, self.length)
        if self._next is None:
            return None
        elif self._next == []:
            return []
        else:
            self._next[index] = next

    def append(self, item):
        if item is None:
            return
        if self.head == 0:
            self.head = 1
            self.length = 1
            self.all_value = [item]
            self.all_next = [0]
        else:
            for i in range(self.length):
                if self.all_next[i] == 0:
                    self.length += 1
                    self.all_value.append(item)
                    self.all_next[i] = self.length
                    self.all_next.append(0)
                    break

    def insert(self, index, item):
        if index >= self.length:
            self.append(item)
            return
        index = Tool.adjust(index, self.length)

        self._length += 1
        if index > 0:
            for i in range(self.length):
                if self._next[i] == index:
                    self._value.append(item)
                    self._next[index-1] = self.length
                    self._next.append(index+1)
        else:
            self.all_value.append(item)
            self.all_next.append(self.head)
            self.head = self.length

    def insert_by_sort(self, node, order=True):
        self.back()
        # 先找到头节点
        pointer = self.head
        if pointer is not None:
            if order:
                # 从头向尾，找到 _value 比节点数大的地方
                while pointer is not None and node._value < pointer._value:
                    pre_pointer = pointer
                    pointer = pointer._next
            else:
                # 从头向尾，找到 _value 比节点数小的地方
                while pointer is not None and node._value > pointer._value:
                    pre_pointer = pointer
                    pointer = pointer._next
            if pointer is not None:
                # 从中间插入
                if pointer != self._head:
                    pre_pointer._next = node
                    node._next = pointer
                # 从头部插入
                else:
                    node._next = self._head
                    self._head = node
            # 从尾部追加
            else:
                pre_pointer._next = node
        # 插入空列表
        else:
            self._head = node
        self._length += 1
        self.back()

    def pop(self, index=0):
        index = Tool.adjust(index, self.length)

        self._length -= 1
        if index > 0:
            for i in range(self.length):
                if self.get_next(i) == index + 1:
                    self.set_next(i, self.get_next(i + 1))
                    self.set_next(i + 1, -1)
                    break

    # @pysnooper.snoop(watch=("_start"))
    def back(self, start=0, end=-1):
        # print("_length = {}".format(self._length))
        if end < 0 or end >= self._length:
            end = self._length - 1
        elif start >= self._length - 1 or end <= start or end == 0:
            return
        _head = self._head
        _prev = None
        _curr = self._head
        if _curr is None:
            return
        i = 0
        if start > 0:
            while i < start:
                _prev = _curr
                _curr = _curr._next
                i += 1
            _start = _prev
            _end = _curr
        else:
            i = -1
        while i <= end and _curr is not None:
            _next = _curr._next
            _curr._next = _prev
            _prev = _curr
            _curr = _next
            i += 1
        if start > 0:
            _start._next = _prev
            _end._next = _curr
        else:
            _head = _prev
        self._head = _head

    # @pysnooper.snoop(watch=("node"))
    def _recursion(self, node, tail, _length):
        if _length <= 0:
            tail = node._next
            return node, tail
        if node is None or node._next is None:
            tail = None
            return node, tail
        _length -= 1
        _head, tail = self._recursion(node._next, tail, _length)
        node._next._next = node
        node._next = None
        return _head, tail

    # @pysnooper.snoop(watch=("start", "end", "_prev", "_tail"))
    def reversed(self, start=0, end=-1):
        if end < 0 or end >= self._length:
            end = self._length - 1
        elif start >= self._length - 1 or end <= start or end == 0:
            return
        _head = self._head
        _prev = None
        _curr = self._head
        _tail = None
        i = 0
        if start > 0:
            while i < start:
                _prev = _curr
                _curr = _curr._next
                i += 1
            _start = _curr
        else:
            i = -1
            _start = self._head
        _curr, _tail = self._recursion(_start, _tail, end - start)
        if start > 0:
            _prev._next._next = _tail
            _prev._next = _curr
        else:
            _head = _curr
        self._head = _head

    def print(self, show=True):
        if self.all_value is None:
            return None
        elif self.all_value == []:
            return []
        result = []
        index = self.head - 1
        while self._next[index] != 0:
            result.append(self._value[index])
            index = self._next[index] - 1
        result.append(self._value[index])
        if show:
            debug(f"result = {result}")
        return result


class TestImitateList:
    @pytest.mark.parametrize("nums",
                             [[2, 3, 5, 8, 9, 10, 18, 26, 32],
                              [],
                              None])
    def test_print(self, nums):
        lst = ImitateList(nums)
        assert lst.print(False) == nums

    @pytest.mark.parametrize("nums", [[2, 3, 5, 8, 9, 10, 18, 26, 32], []])
    def test_len(self, nums):
        lst = ImitateList(nums)
        assert len(lst) == len(nums)

    @pytest.mark.parametrize("nums",
                             [[2, 3, 5, 8, 9, 10, 18, 26, 32],
                              [],
                              None])
    def test_get_all_value(self, nums):
        lst = ImitateList(nums)
        assert lst.all_value == nums

    @pytest.mark.parametrize("nums",
                             [[2, 3, 5, 8, 9, 10, 18, 26, 32],
                              [],
                              None])
    def test_get_all_next(self, nums):
        lst = ImitateList(nums)
        assert lst.all_next == lst._next

    @pytest.mark.parametrize("nums, index",
                             [([2, 3, 5, 8, 9, 10, 18, 26, 32], 6),
                              ([], 4)])
    def test_get_value(self, nums, index):
        lst = ImitateList(nums)
        if nums == []:
            assert lst.get_value(index) == []
        else:
            assert lst.get_value(index) == nums[index]

    @pytest.mark.parametrize("nums, index, item",
                             [([2, 3, 5, 8, 9, 10, 18, 26, 32], 3, 6),
                              ([2, 3, 5, 8, 9, 10, 18, 26, 32], -3, 6),
                              ([2, 3, 5, 8, 9, 10, 18, 26, 32], -18, 6),
                              ([], 8, 4)])
    def test_set_value(self, nums, index, item):
        lst = ImitateList(nums)
        lst.set_value(index, item)
        if nums == []:
            assert lst.get_value(index) == []
        else:
            index = Tool.adjust(index, len(nums))
            nums[index] = item
            assert lst.print(False) == nums

    @pytest.mark.parametrize("nums, index",
                             [([2, 3, 5, 8, 9, 10, 18, 26, 32], 6),
                              ([], 4)])
    def test_get_next(self, nums, index):
        lst = ImitateList(nums)
        lst.get_next(index)
        if nums == []:
            assert lst.get_next(index) == []
        else:
            assert lst.get_next(index) == lst._next[index]

    @pytest.mark.parametrize("nums, index, item",
                             [([2, 3, 5, 8, 9, 10, 18, 26, 32], 3, 6),
                              ([2, 3, 5, 8, 9, 10, 18, 26, 32], -3, 6),
                              ([2, 3, 5, 8, 9, 10, 18, 26, 32], -18, 6),
                              ([], 8, 4)])
    def test_set_next(self, nums, index, item):
        lst = ImitateList(nums)
        lst.set_next(index, item)
        if nums == []:
            assert lst.get_next(index) == []
        else:
            index = Tool.adjust(index, len(nums))
            nums[index] = item
            assert lst.get_next(index) == lst._next[index]

    @pytest.mark.parametrize("nums, item",
                             [([2, 3, 5, 8, 9, 10, 18, 26, 32], 6),
                              ([], 4)])
    def test_append(self, nums, item):
        lst = ImitateList(nums)
        lst.append(item)
        nums.append(item)
        assert lst.print(False) == nums

    @pytest.mark.parametrize("nums, index, item",
                             [([2, 3, 5, 8, 9, 10, 18, 26, 32], 3, 6),
                              ([2, 3, 5, 8, 9, 10, 18, 26, 32], -3, 6),
                              ([2, 3, 5, 8, 9, 10, 18, 26, 32], -18, 6),
                              ([], 8, 4)])
    def test_insert(self, nums, index, item):
        lst = ImitateList(nums)
        lst.insert(index, item)
        nums.insert(index, item)
        assert lst.print(False) == nums

    @pytest.mark.parametrize("nums, index",
                             [([2, 3, 5, 8, 9, 10, 18, 26, 32], 5),
                              ([], 3)])
    def test_get(self, nums, index):
        lst = ImitateList(nums)
        if nums is None or nums == []:
            assert lst[index] is None
        else:
            assert lst[index] == nums[index]

    @pytest.mark.parametrize("nums, item, index",
                             [([2, 3, 5, 8, 9, 10, 18, 26, 32], 99, 5),
                              ([], 55, 3)])
    def test_set(self, nums, item, index):
        lst = ImitateList(nums)
        lst[index] = item
        if nums is None or nums == []:
            assert lst[index] is None
        else:
            nums[index] = item
            assert lst.print(False) == nums

    @pytest.mark.parametrize("nums, index",
                             [([2, 3, 5, 8, 9, 10, 18, 26, 32], 5),
                              ([], 3)])
    def test_pop(self, nums, index):
        lst = ImitateList(nums)
        if nums is None or nums == []:
            assert lst.is_none()
        else:
            lst.pop(index)
            nums.pop(index)
            assert lst.print(False) == nums


class CrossList(List):
    def __init__(self):
        super().__init__()
        self.other = None

    def append(self, _value):
        super().append(_value)
        if self.other is not None:
            self.other._length += 1

    def append_node(self, node):
        if self._head is not None:
            p = self._head
            while p._next is not None:
                p = p._next
            p._next = node
        else:
            self._head = node
        self._length += 1
        if self.other is not None:
            self.other._length += 1

    def cross(self, other, _value):
        node = Node(_value)
        if self.other is None:
            self.append_node(node)
            other.append_node(node)
            self.other = other
            self.other.other = self


class LoopList(List):
    def __init__(self):
        super().__init__()
        self.circle = False
        self.close = None

    def append(self, node):
        if self.circle:
            if self.close == self._head:
                count = 1
            else:
                count = 0
            pointer = self._head
            while count < 2:
                pointer = pointer._next
                if pointer._next == self.close:
                    count += 1
            pointer._next = node
            node._next = self.close
            self._length += 1
        else:
            super().append(node)

    def set_circle(self, index):
        if index > self._length or index < 0:
            return False
        if self._length > 3:
            node = self._head
            for i in range(index):
                node = node._next
            close_node = node
            while node._next is not None:
                node = node._next
            node._next = close_node
            self.circle = True
            self.close = close_node
            return True
        else:
            return False

    def remove(self, index):
        if self.circle:
            if index >= self._length:
                index = self._length - 1
            elif index < 0:
                index = 0
            node = Node()
            if index > 0:
                p = self._head
                n = 0
                while n < index - 1:
                    p = p._next
                    n += 1
                if p._next == self.close:
                    node = p._next
                    p._next = node._next
                    while p._next != self.close:
                        p = p._next
                    p._next = self.close._next
                    self.close = self.close._next
                else:
                    node = p._next
                    p._next = node._next
            else:
                node = self._head
                self._head = node._next
            self._length -= 1
            return node._value
        else:
            super().remove(index)

    def remove_circle(self):
        if self.circle:
            node = self._head
            while node._next != self.close:
                node = node._next
            node._next = None
            self.circle = False
            self.close = None

    def display(self):
        if self.circle:
            print("长度为 {}，在 {} 处环封闭".format(self._length, self.close._value))
        else:
            print("长度为 {}，无环".format(self._length))
        lst = []
        if self.circle:
            if self.close == self._head:
                count = 1
            else:
                count = 0
            node = self._head
            while count < 2:
                if node._next == self.close:
                    count += 1
                lst.append(node._value)
                node = node._next
            print(lst)
            return lst
        else:
            super().display()


class JosephList(LoopList):
    def __init__(self):
        super().__init__()
        self.remove_pointer = None
        self.link_pointer = None

    def _next_pointer(self):
        if self._length > 2:
            if self.remove_pointer is not None:
                self.link_pointer = self.remove_pointer
                self.remove_pointer = self.remove_pointer._next
            else:
                self.remove_pointer = self._head
            return True
        else:
            return False

    def remove(self):
        node = self.remove_pointer
        if node == self._head:
            self._head = node._next
            self.close = node._next
        self.remove_pointer = self.remove_pointer._next
        self.link_pointer._next = node._next
        node._next = None
        self._length -= 1
        print("{} 出队".format(node._value))


class DoubleList(List):
    def __init__(self):
        super().__init__()
        self.tail = None

    def append(self, node):
        # node = DoubleNode(_value)
        if self._head is not None:
            self.tail._next = node
            node.pre = self.tail
            self.tail = node
        else:
            self._head = node
            self.tail = node
        self._length += 1

    def insert(self, node, index=0):
        if index >= self._length:
            self.append(node)
            return
        elif index < 0:
            index = 0
        # node = DoubleNode(_value)
        if index > 0:
            p = self._head
            n = 0
            while n < index - 1:
                p = p._next
                n += 1
            node._next = p._next
            p._next.pre = node
            p._next = node
            node.pre = p
        else:
            node._next = self._head
            self._head.pre = node
            self._head = node
        self._length += 1

    def insert_by_sort(self, node, order=True):
        # 先找到头节点
        pointer = self._head
        if pointer is not None:
            if order:
                # 从头向尾，找到 _value 比节点数大的地方
                while pointer is not None and node._value > pointer._value:
                    pointer = pointer._next
            else:
                # 从头向尾，找到 _value 比节点数小的地方
                while pointer is not None and node._value < pointer._value:
                    pointer = pointer._next
            if pointer is not None:
                # 从中间插入
                if pointer != self._head:
                    temp_node = pointer.pre
                    pointer.pre = node
                    node._next = pointer
                    node.pre = temp_node
                    temp_node._next = node
                # 从头部插入
                else:
                    node._next = self._head
                    self._head.pre = node
                    self._head = node
            # 从尾部追加
            else:
                self.tail._next = node
                node.pre = self.tail
                self.tail = node
        # 插入空列表
        else:
            self._head = node
            self.tail = node
        self._length += 1

    def remove(self, index=0):
        node = None

        # 返回空链表
        if self._length == 0:
            return None

        # 删除尾节点
        if index >= (self._length - 1):
            index = self._length - 1
            node = self.tail
            if node.pre is not None:
                self.tail = node.pre
                self.tail._next = None
            else:
                self._head = None
                self.tail = None

        # 删除头节点
        elif index <= 0:
            index = 0
            node = self._head
            if node._next is not None:
                self._head = node._next
                self._head.pre = None
            else:
                self._head = None
                self.tail = None

        # 删除中间节点
        else:
            node = self._head
            n = 0
            while n < index:
                node = node._next
                n += 1
            node.pre._next = node._next
            node._next.pre = node.pre
        self._length -= 1
        return node._value

    def back_display(self):
        lst = []
        node = self.tail
        while node is not None:
            lst.append(node._value)
            node = node.pre
        print(lst)
        return lst


class LoopDoubleList(DoubleList, LoopList):
    @staticmethod
    def concat_lists(*lists):
        res = List()
        for i in lists:
            node = i._head
            while node is not None:
                res.append(Node(node._value))
                res._length += 1
                node = node._next
        return res

    @staticmethod
    def concat_order_lists(*lists):
        res = List()
        for i in lists:
            node = i._head
            while node is not None:
                res.append(Node(node._value))
                res._length += 1
                node = node._next
        return res

    @staticmethod
    def get_cross(a, b):
        pa = a._head
        pb = b._head
        while pa._next is not None:
            pa = pa._next
        while pb._next is not None:
            pb = pb._next
        if pa == pb:
            print("相交")
            diff = abs(a._length - b._length)
            pa = a._head
            pb = b._head
            len = a._length
            if diff > 0:
                if a._length > b._length:
                    for i in range(diff):
                        pa = pa._next
                    len = a._length
                else:
                    for i in range(diff):
                        pb = pb._next
                    len = b._length
            for i in range(len):
                if pa != pb:
                    pa = pa._next
                    pb = pb._next
                else:
                    print("相交点：{}".format(pa._value))
                    break
        else:
            print("不相交")

    def __init__(self):
        DoubleList.__init__(self)
        LoopList.__init__(self)

    def append(self, node):
        if self._head is not None:
            self.tail._next = node
            node.pre = self.tail
            node._next = self._head
            self._head.pre = node
            self.tail = node
        else:
            node._next = node
            node.pre = node
            self._head = node
            self.tail = node
        self._length += 1

    def insert(self, node, index=0):
        if index >= self._length:
            self.append(node)
            return
        elif index < 0:
            index = 0
        if index > 0:
            pointer = self._head
            n = 0
            while n < (index - 1):
                pointer = pointer._next
                n += 1
            insert_node = pointer._next
            pointer._next = node
            node.pre = pointer
            node._next = insert_node
            insert_node.pre = node
        else:
            node._next = self._head
            self._head.pre = node
            self._head = node
            self.tail._next = node
            node.pre = self.tail
        self._length += 1

    def remove(self, index=0):
        node = None
        if self._length == 0:
            return None

        # 删除尾节点
        if index >= (self._length - 1):
            node = self.tail

            # 链表中有多个节点
            if self._length > 1:
                self.tail = node.pre
                node.pre._next = self._head
                self._head.pre = node.pre
                node.pre = None
                node._next = None

            # 链表中只有一个节点
            else:
                node.pre = None
                node._next = None
                self._head = None
                self.tail = None
            self._length -= 1
            return node._value

        # 删除头节点
        elif index <= 0:
            node = self._head
            if self._length > 1:
                self._head = node._next
                self._head.pre = self.tail
                self.tail._next = self._head
                node._next = None
                node.pre = None
            else:
                node.pre = None
                node._next = None
                self._head = None
                self.tail = None
            self._length -= 1
            return node._value

        # 删除中间节点
        else:
            pointer = self._head
            n = 0
            while n < index:
                pointer = pointer._next
                n += 1
            node = pointer
            node.pre._next = node._next
            node._next.pre = node.pre
            node.pre = None
            node._next = None
            self._length -= 1
            return node._value

    def display(self):
        LoopList.display(self)

    def back_display(self):
        pass


if __name__ == "__main__":
    nums = [2, 3, 5, 8, 9, 10, 18, 26, 32]
    t1 = List(nums)
    t2 = List(nums)
    t3 = List(nums)
    debug(f"t3.head.counter() = {t1.head.counter}")
    t1.print()
    debug(f"这是一条信息。")
    o = Node(6)
    debug(f"object = {o.value}")
