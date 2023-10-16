from jasonqwu_lib import *


def decrypt(nums):
    """
    >>> decrypt([0,6,3,1,7,5,8,9,2,4])
    [6, 1, 5, 9, 4, 7, 2, 8, 3]
    """
    head = 1
    tail = len(nums) - 1
    result = []
    while head < tail:
        result.append(nums[head])
        nums.append(nums[head+1])
        tail += 1
        head += 2
    result.append(nums[head])
    return result


if __name__ == '__main__':
    nums = get_array("请输入一个整数数组：")
    print(decrypt(nums))
