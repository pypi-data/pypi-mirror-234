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

def test_cuda_awkward_ByteMaskedArray_toIndexedOptionArray64_1():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    mask = cupy.array([1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_toIndexedOptionArray', cupy.int64, cupy.int8]
    funcC(toindex, mask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 1, 2]
    assert cupy.array_equal(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cuda_awkward_ByteMaskedArray_toIndexedOptionArray64_2():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    mask = cupy.array([0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    validwhen = False
    funcC = cupy_backend['awkward_ByteMaskedArray_toIndexedOptionArray', cupy.int64, cupy.int8]
    funcC(toindex, mask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 1, 2]
    assert cupy.array_equal(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cuda_awkward_ByteMaskedArray_toIndexedOptionArray64_3():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    mask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_toIndexedOptionArray', cupy.int64, cupy.int8]
    funcC(toindex, mask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 1, 2]
    assert cupy.array_equal(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cuda_awkward_ByteMaskedArray_toIndexedOptionArray64_4():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    mask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_toIndexedOptionArray', cupy.int64, cupy.int8]
    funcC(toindex, mask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 1, 2]
    assert cupy.array_equal(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cuda_awkward_ByteMaskedArray_toIndexedOptionArray64_5():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    mask = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_toIndexedOptionArray', cupy.int64, cupy.int8]
    funcC(toindex, mask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [-1, -1, -1]
    assert cupy.array_equal(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

