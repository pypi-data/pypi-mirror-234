import pytest


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        return None


def list_to_node(list):
    l1 = ListNode(list[0])
    for i in list:
        pass


def node_to_list(node):
    pass


# @pytest.mark.leetcode
@pytest.mark.parametrize("in1, in2, expected",
                         [([2, 4, 3], [5, 6, 4], [7, 0, 8]),
                          ([0], [0], [0]),
                          ([9, 9, 9, 9, 9, 9, 9],
                           [9, 9, 9, 9],
                           [8, 9, 9, 9, 0, 0, 0, 1])])
def test_addTwoNumbers(in1, in2, expected):
    s = Solution()
    print()
    print(type(in1))
    l1 = list_to_node(in1)
    print(l2)
    l2 = list_to_node(in2)
    node = s.addTwoNumbers(l1, l2)
    res = node_to_list(node)
    print(s.addTwoNumbers(l1, l2))
    assert res == expected
