'''
二分法是一种效率比较高的搜索方法
回忆之前做过的猜数字的小游戏，预先给定一个小于100的正整数 x，让你猜，猜测过程中给予大小判断的提示，问你怎样快速地猜出来？
我们之前做的游戏给定的是10次机会，如果我们学会二分查找法以后，不管数字是多少，最多只需要7次就能猜到数字。
'''
def binary_searching(arr, num):
    count = 0
    left = 0
    right = len(arr)
    while left <= right:
        middle = (left + right) // 2
        count += 1
        if num > arr[middle]:
            left = middle + 1
        elif num < arr[middle]:
            right = middle - 1
        else:
            return middle, count
    return -1, count
