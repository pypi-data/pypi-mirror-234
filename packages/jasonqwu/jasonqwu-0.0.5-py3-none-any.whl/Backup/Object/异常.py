import time

class UnexceptedCancle(Exception):
    def __str__(self):
        return "意外终止"

try:
    with open("test.txt") as f:
        try:
            while True:
                content = f.readline()
                if len(content) == 0:
                    break
                time.sleep(2)
                print(content)
        except:
            raise UnexceptedCancle()
except FileNotFoundError:
    with open("test.txt", 'a') as f:
        f.write("aaa")
except UnexceptedCancle as cancle:
    print(cancle)
else:
    print("没有异常，真开心。")
finally:
    print("这里是finally.")

try:
    print(num)
except Exception as result:
    print(result)

try:
    print(num)
except (NameError, ZeroDivisionError) as result:
    num = 5
    print(num)

try:
    print(1 / 0)
except (NameError, ZeroDivisionError) as result:
    print("除数为零。")
    print(result)
