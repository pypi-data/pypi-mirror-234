import pytest
import vector_lib

def setup_module():
    print("\n *** 初始化-模块 Vector ***")

def teardown_module():
    print("\n *** 清除-模块 Vector ***")

@pytest.mark.lib
@pytest.mark.parametrize(
    "dim, expected",
    [
        (5, [0, 0, 0, 0, 0]),
        (7, [0, 0, 0, 0, 0, 0, 0])
    ]
)
def test_zero(dim, expected):
    vec = vector_lib.Vector.zero(dim)
    assert vec == expected

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([5, 7, 11, 22, 27, 33, 39, 52, 58], [5, 7, 11, 22, 27, 33, 39, 52, 58]),
        ([15, 27, 131, 122, 8], [15, 27, 131, 122, 8]),
    ]
)
def test_init(arr, expected):
    vec = vector_lib.Vector(arr)
    assert (vec) == expected

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([5, 7, 11, 22, 27, 33, 39, 52, 58], [5, 7, 11, 22, 27, 33, 39, 52, 58]),
        ([15, 27, 131, 122, 8], [15, 27, 131, 122, 8]),
    ]
)
def test_repr(arr, expected):
    vec = vector_lib.Vector(arr)
    assert vec == expected

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([5, 7, 11, 22, 27, 33, 39, 52, 58], "(5, 7, 11, 22, 27, 33, 39, 52, 58)"),
        ([15, 27, 131, 122, 8], "(15, 27, 131, 122, 8)"),
    ]
)
def test_str(arr, expected):
    vec = vector_lib.Vector(arr)
    assert str(vec) == expected

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([5, 7, 11, 22, 27, 33, 39, 52, 58], 9),
        ([15, 27, 131, 122, 8], 5),
    ]
)
def test_len(arr, expected):
    vec = vector_lib.Vector(arr)
    assert len(vec) == expected

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([5, 7, 11, 22, 27, 33, 39, 52, 58], 27),
        ([15, 27, 131, 122, 8], 8),
    ]
)
def test_iter(arr, expected):
    vec = vector_lib.Vector(arr)
    count = 0
    res = None
    for i in vec:
        count += 1
        if count == 5:
            res = i
            break
    assert res == expected

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr1, arr2",
    [
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([5, 4, 3, 2, 1], [5, 4, 3, 2, 1])
    ]
)
def test_eq(arr1, arr2):
    vec1 = vector_lib.Vector(arr1)
    vec2 = vector_lib.Vector(arr2)
    assert vec1 == vec2

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([1, 2, -3, 4, 5], [-1, -2, 3, -4, -5]),
        ([5, -14, 3, -2, 1], [-5, 14, -3, 2, -1])
    ]
)
def test_neg(arr, expected):
    vec = vector_lib.Vector(arr)
    assert -vec == expected

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, index, expected",
    [
        ([5, 7, 11, 22, 27, 33, 39, 52, 58], 4, 27),
        ([15, 27, 131, 122, 8], 3, 122),
    ]
)
def test_getitem(arr, index, expected):
    vec = vector_lib.Vector(arr)
    assert vec[index] == expected

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr1, arr2, expected",
    [
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [2, 4, 6, 8, 10]),
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [6, 6, 6, 6, 6])
    ]
)
def test_add(arr1, arr2, expected):
    vec1 = vector_lib.Vector(arr1)
    vec2 = vector_lib.Vector(arr2)
    assert vec1 + vec2 == vector_lib.Vector(expected)

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr1, arr2, expected",
    [
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [0, 0, 0, 0, 0]),
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [-4, -2, 0, 2, 4])
    ]
)
def test_sub(arr1, arr2, expected):
    vec1 = vector_lib.Vector(arr1)
    vec2 = vector_lib.Vector(arr2)
    assert vec1 -vec2 == vector_lib.Vector(expected)

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, scalar, expected",
    [
        ([1, 2, 3, 4, 5], 2, [2, 4, 6, 8, 10]),
        ([1, 2, 3, 4, 5], 3, [3, 6, 9, 12, 15])
    ]
)
def test_mul(arr, scalar, expected):
    vec = vector_lib.Vector(arr)
    assert scalar * vec == vector_lib.Vector(expected)

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, scalar, expected",
    [
        ([12, 24, 36, 72, 108], 2, [24, 48, 72, 144, 216]),
        ([3, 24, 36, 72, 108], 3, [9, 72, 108, 216, 324])
    ]
)
def test_rmul(arr, scalar, expected):
    vec = vector_lib.Vector(arr)
    assert vec * scalar == vector_lib.Vector(expected)

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, scalar, expected",
    [
        ([12, 24, 36, 72, 108], 2, [6, 12, 18, 36, 54]),
        ([3, 24, 36, 72, 108], 3, [1, 8, 12, 24, 36])
    ]
)
def test_truediv(arr, scalar, expected):
    vec = vector_lib.Vector(arr)
    assert vec / scalar == vector_lib.Vector(expected)

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr1, arr2",
    [
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]),
        ([1, 2, 3, 4, 5], [5, 4, 3, 2])
    ]
)
def test_error(arr1, arr2):
    vec1 = vector_lib.Vector(arr1)
    vec2 = vector_lib.Vector(arr2)
    with pytest.raises(AssertionError):
        vec = vec1 + vec2
    with pytest.raises(AssertionError):
        vec = vec1 - vec2
    with pytest.raises(AssertionError):
        vec = vec1.dot(vec2)

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([5, 2], 5.385164807134504),
        ([3, 1], 3.1622776601683795),
        ([0, 0], 0.0),
    ]
)
def test_norm(arr, expected):
    vec = vector_lib.Vector(arr)
    assert vec.norm() == expected

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([5, 2], (0.9284766908852593, 0.3713906763541037)),
        ([3, 1], (0.9486832980505138, 0.31622776601683794)),
        ([0, 0], (0, 0)),
    ]
)
def test_normalize(arr, expected):
    vec = vector_lib.Vector(arr)
    assert vec.normalize() == expected

@pytest.mark.lib
@pytest.mark.parametrize(
    "arr1, arr2, expected",
    [
        ([1, 2, 3], [2, 3, 5], 23),
        ([4, 5], [4, 2], 26)
    ]
)
def test_dot(arr1, arr2, expected):
    vec1 = vector_lib.Vector(arr1)
    vec2 = vector_lib.Vector(arr2)
    assert vec1.dot(vec2) == expected
