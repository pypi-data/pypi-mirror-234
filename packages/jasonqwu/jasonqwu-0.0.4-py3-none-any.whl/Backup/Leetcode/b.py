name = "root"


def func():
    def inner():
        print(name)
        return "admin"

    return inner


v = func()
result = v()
print(result)