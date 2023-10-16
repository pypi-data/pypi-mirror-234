import pytest


class Solution:
    '''
        1. 两数之和
        给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target 的那两个整数，并返回它们的数组下标。

        你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。

        你可以按任意顺序返回答案。
    '''
    def twoSum(self, nums, target: int):
        result = []
        for _1, _2 in enumerate(nums):
            if target - _2 in nums[_1 + 1:]:
                result.append(_1)
                result.append(_1 +
                              nums[_1 + 1:].index(target - _2) +
                              1 if target - _2 == _2
                              else nums.index(target - _2))
                return result


# @pytest.mark.leetcode
@pytest.mark.order(1)
# @pytest.mark.skip(reason="不需要")
@pytest.mark.parametrize("nums, target, expected",
                         [([2, 7, 11, 15], 9, [0, 1]),
                          ([3, 2, 4], 6, [1, 2]),
                          ([3, 3], 6, [0, 1])])
def test_twoSum(nums, target, expected):
    s = Solution()
    print()
    print(f"nums = {nums}")
    print(f"target = {target}")
    print(s.twoSum(nums, target))
    assert s.twoSum(nums, target) == expected
