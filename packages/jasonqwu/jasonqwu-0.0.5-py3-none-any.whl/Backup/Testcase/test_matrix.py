import pytest
import matrix_lib


def setup_module():
    print("\n *** 初始化-模块 Matrix ***")


def teardown_module():
    print("\n *** 清除-模块 Matrix ***")


@pytest.mark.lib
@pytest.mark.parametrize(
    "r, c, expected",
    [
        (3, 2, [[0, 0], [0, 0], [0, 0]]),
    ]
)
def test_zero(r, c, expected):
    mtx = matrix_lib.Matrix.zero(r, c)
    assert mtx == expected


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([[1, 2], [3, 4]], [[1, 2], [3, 4]]),
    ]
)
def test_init(arr, expected):
    mtx = matrix_lib.Matrix(arr)
    assert (mtx) == expected

# @pytest.mark.lib
# @pytest.mark.parametrize(
#     "arr, expected",
#     [
#         ([5, 7, 11, 22, 27, 33, 39, 52, 58],
#          [5, 7, 11, 22, 27, 33, 39, 52, 58]),
#         ([15, 27, 131, 122, 8], [15, 27, 131, 122, 8]),
#     ]
# )
# def test_repr(arr, expected):
#     mtx = matrix_lib.Matrix(arr)
#     assert mtx == expected

# @pytest.mark.lib
# @pytest.mark.parametrize(
#     "arr, expected",
#     [
#         ([5, 7, 11, 22, 27, 33, 39, 52, 58],
#          "(5, 7, 11, 22, 27, 33, 39, 52, 58)"),
#         ([15, 27, 131, 122, 8], "(15, 27, 131, 122, 8)"),
#     ]
# )
# def test_str(arr, expected):
#     mtx = matrix_lib.Matrix(arr)
#     assert str(mtx) == expected


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([[5, 7, 11, 22], [27, 33, 39, 52]], 8),
    ]
)
def test_len(arr, expected):
    mtx = matrix_lib.Matrix(arr)
    assert len(mtx) == expected

# @pytest.mark.lib
# @pytest.mark.parametrize(
#     "arr, expected",
#     [
#         ([5, 7, 11, 22, 27, 33, 39, 52, 58], 27),
#         ([15, 27, 131, 122, 8], 8),
#     ]
# )
# def test_iter(arr, expected):
#     mtx = matrix_lib.Matrix(arr)
#     count = 0
#     res = None
#     for i in mtx:
#         count += 1
#         if count == 5:
#             res = i
#             break
#     assert res == expected

# @pytest.mark.lib
# @pytest.mark.parametrize(
#     "arr1, arr2",
#     [
#         ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
#         ([5, 4, 3, 2, 1], [5, 4, 3, 2, 1])
#     ]
# )
# def test_eq(arr1, arr2):
#     mtx1 = matrix_lib.Matrix(arr1)
#     mtx2 = matrix_lib.Matrix(arr2)
#     assert mtx1 == mtx2


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([[1, 2], [-3, 4], [5, -9]], [[1, 2], [-3, 4], [5, -9]]),
    ]
)
def test_pos(arr, expected):
    mtx = matrix_lib.Matrix(arr)
    assert mtx == matrix_lib.Matrix(expected)


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([[1, 2], [-3, 4], [5, -9]], [[-1, -2], [3, -4], [-5, 9]]),
    ]
)
def test_neg(arr, expected):
    mtx = matrix_lib.Matrix(arr)
    assert -mtx == matrix_lib.Matrix(expected)


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, pos, expected",
    [
        ([[5, 7, 11, 22], [27, 33, 52, 58]], (1, 2), 52),
    ]
)
def test_getitem(arr, pos, expected):
    mtx = matrix_lib.Matrix(arr)
    assert mtx[pos] == expected


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr1, arr2, expected",
    [
        ([[1, 2], [3, 4], [5, 7]],
         [[1, 2], [3, 4], [5, 7]],
         [[2, 4], [6, 8], [10, 14]]),
    ]
)
def test_add(arr1, arr2, expected):
    mtx1 = matrix_lib.Matrix(arr1)
    mtx2 = matrix_lib.Matrix(arr2)
    assert mtx1 + mtx2 == matrix_lib.Matrix(expected)


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr1, arr2, expected",
    [
        ([[5, 4], [6, 8], [9, 1]],
         [[1, 2], [3, 4], [5, 7]],
         [[4, 2], [3, 4], [4, -6]]),
    ]
)
def test_sub(arr1, arr2, expected):
    mtx1 = matrix_lib.Matrix(arr1)
    mtx2 = matrix_lib.Matrix(arr2)
    assert mtx1 - mtx2 == matrix_lib.Matrix(expected)


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, scalar, expected",
    [
        ([[1, 2], [3, 4], [5, 7]], 2, [[2, 4], [6, 8], [10, 14]]),
    ]
)
def test_mul(arr, scalar, expected):
    mtx = matrix_lib.Matrix(arr)
    assert scalar * mtx == matrix_lib.Matrix(expected)


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, scalar, expected",
    [
        ([[1, 2], [3, 4], [5, 7]], 2, [[2, 4], [6, 8], [10, 14]]),
    ]
)
def test_rmul(arr, scalar, expected):
    mtx = matrix_lib.Matrix(arr)
    assert mtx * scalar == matrix_lib.Matrix(expected)


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, scalar, expected",
    [
        ([[12, 24], [36, 72], [108, 4]], 2, [[6, 12], [18, 36], [54, 2]]),
    ]
)
def test_truediv(arr, scalar, expected):
    mtx = matrix_lib.Matrix(arr)
    assert mtx / scalar == matrix_lib.Matrix(expected)

# @pytest.mark.lib
# @pytest.mark.parametrize(
#     "arr1, arr2",
#     [
#         ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]),
#         ([1, 2, 3, 4, 5], [5, 4, 3, 2])
#     ]
# )
# def test_error(arr1, arr2):
#     mtx1 = matrix_lib.Matrix(arr1)
#     mtx2 = matrix_lib.Matrix(arr2)
#     with pytest.raises(AssertionError):
#         mtx = mtx1 + mtx2
#     with pytest.raises(AssertionError):
#         mtx = mtx1 - mtx2
#     with pytest.raises(AssertionError):
#         mtx = mtx1.dot(mtx2)


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([[5, 2], [2, 6]], (2, 2)),
    ]
)
def test_shape(arr, expected):
    mtx = matrix_lib.Matrix(arr)
    assert mtx.shape() == expected


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([[5, 2], [2, 6], [2, 6]], 3),
    ]
)
def test_row_num(arr, expected):
    mtx = matrix_lib.Matrix(arr)
    assert mtx.row_num() == expected


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([[5, 2], [2, 6]], 2),
    ]
)
def test_col_num(arr, expected):
    mtx = matrix_lib.Matrix(arr)
    assert mtx.col_num() == expected


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([[5, 2], [2, 7]], [2, 7]),
    ]
)
def test_row_vector(arr, expected):
    mtx = matrix_lib.Matrix(arr)
    assert mtx.row_vector(1) == expected


@pytest.mark.lib
@pytest.mark.parametrize(
    "arr, expected",
    [
        ([[5, 2], [2, 7]], [2, 7]),
    ]
)
def test_col_vector(arr, expected):
    mtx = matrix_lib.Matrix(arr)
    assert mtx.col_vector(1) == expected

# @pytest.mark.lib
# @pytest.mark.parametrize(
#     "arr, expected",
#     [
#         ([5, 2], (0.9284766908852593, 0.3713906763541037)),
#         ([3, 1], (0.9486832980505138, 0.31622776601683794)),
#         ([0, 0], (0, 0)),
#     ]
# )
# def test_normalize(arr, expected):
#     mtx = matrix_lib.Matrix(arr)
#     assert mtx.normalize() == expected

# @pytest.mark.lib
# @pytest.mark.parametrize(
#     "arr1, arr2, expected",
#     [
#         ([1, 2, 3], [2, 3, 5], 23),
#         ([4, 5], [4, 2], 26)
#     ]
# )
# def test_dot(arr1, arr2, expected):
#     mtx1 = matrix_lib.Matrix(arr1)
#     mtx2 = matrix_lib.Matrix(arr2)
#     assert mtx1.dot(mtx2) == expected
