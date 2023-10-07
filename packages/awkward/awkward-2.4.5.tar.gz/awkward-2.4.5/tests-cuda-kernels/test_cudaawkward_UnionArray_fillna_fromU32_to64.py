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

def test_cuda_awkward_UnionArray_fillna_fromU32_to64_1():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_fillna', cupy.int64, cupy.uint32]
    funcC(toindex, fromindex, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [1, 0, 0]
    assert cupy.array_equal(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cuda_awkward_UnionArray_fillna_fromU32_to64_2():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromindex = cupy.array([1, 2, 2, 3, 0, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_fillna', cupy.int64, cupy.uint32]
    funcC(toindex, fromindex, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [1, 2, 2]
    assert cupy.array_equal(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cuda_awkward_UnionArray_fillna_fromU32_to64_3():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromindex = cupy.array([1, 3, 0, 3, 5, 2, 0, 2, 1, 1], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_fillna', cupy.int64, cupy.uint32]
    funcC(toindex, fromindex, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [1, 3, 0]
    assert cupy.array_equal(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cuda_awkward_UnionArray_fillna_fromU32_to64_4():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_fillna', cupy.int64, cupy.uint32]
    funcC(toindex, fromindex, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [1, 4, 2]
    assert cupy.array_equal(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cuda_awkward_UnionArray_fillna_fromU32_to64_5():
    toindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    length = 3
    funcC = cupy_backend['awkward_UnionArray_fillna', cupy.int64, cupy.uint32]
    funcC(toindex, fromindex, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_toindex = [0, 0, 0]
    assert cupy.array_equal(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

