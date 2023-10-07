# AUTO GENERATED ON 2023-09-28 AT 16:44:16
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import cupy
import pytest

import awkward as ak
import awkward._connect.cuda as ak_cu

cupy_backend = ak._backends.CupyBackend.instance()

def test_cuda_awkward_RegularArray_getitem_next_at_64_1():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    at = 0
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_at', cupy.int64]
    funcC(tocarry, at, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 3, 6]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_next_at_64_2():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    at = 0
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_at', cupy.int64]
    funcC(tocarry, at, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 3, 6]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_next_at_64_3():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    at = 2
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_at', cupy.int64]
    funcC(tocarry, at, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 5, 8]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_next_at_64_4():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    at = 1
    length = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_next_at', cupy.int64]
    funcC(tocarry, at, length, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 4, 7]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

