import pytest
import algorithm_lib

def setup_module():
    print("\n *** 初始化-模块 ***")

def teardown_module():
    print("\n *** 清除-模块 ***")

def func(x):
    if x == 0:
        raise ValueError("value error!")
    else:
        pass

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, num, expected",
    [
        ([5, 7, 11, 22, 27, 33, 39, 52, 58], 11, (2, 3)),
        ([5, 7, 11, 22, 27, 33, 39, 52, 58], 13, (-1, 4)),
    ]
)
def test_binary_searching(arr, num, expected):
    assert algorithm_lib.binary_searching(arr, num) == expected

def test_raises():
    with pytest.raises(ValueError):
        func(0)

def test_func_none():
    assert func(1) == None
