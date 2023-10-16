from collections.abc import *

class Ranges():
    def __init__(self, end):
        self.start = 0
        self.end = end

    def __next__(self):
        if self.start < self.end:
            curr = self.start
            self.start += 1
            return curr
        else:
            raise StopIteration

    def __iter__(self):
        return self

def my_range(end):
    start = 0
    while start < end:
        yield start
        start += 1

myra = Ranges(5)
myran = my_range(3)
print(isinstance(myra, Iterable))
print(isinstance(myra, Iterator))

print(isinstance(myran, Iterable))
print(isinstance(myran, Iterator))
print(next(myra))
print(next(myra))
print("1111")
for i in myra:
    print(i)
# print(next(myra))
print(next(myran))
for i in myran:
    print(i)
