import dis



def maxOfThreeNumbers1(self, num1, num2, num3):
    # write your code here
    ret = max(num1, num2)
    ret = max(ret, num3)
    return ret


def maxOfThreeNumbers2(self, num1, num2, num3):
    # write your code here
    ret = num1
    if ret < num2:
        ret = num2
    if ret < num3:
        ret = num3
    return ret


if __name__ == '__main__':
    # s1 = Solution1()
    # s2 = Solution2()
    # nums = [2, 7, 11, 15]
    # target = 9
    # for _ in s1.twoSum(nums, target):
    print(dis.dis(maxOfThreeNumbers1))
    print("================")
    print(dis.dis(maxOfThreeNumbers2))
    # # nums = [3, 2, 4]
    # target = 6
    # print(dis.dis(s1.twoSum(nums, target)))
    # print("================")
    # print(dis.dis(s2.twoSum(nums, target)))
    # nums = [3, 3]
    # target = 6
    # print(dis.dis(s1.twoSum(nums, target)))
    # print("================")
    # print(dis.dis(s2.twoSum(nums, target)))
    # nums = [2, 5, 5, 11]
    # target = 10
    # print(dis.dis(s1.twoSum(nums, target)))
    # print("================")
    # print(dis.dis(s2.twoSum(nums, target)))
