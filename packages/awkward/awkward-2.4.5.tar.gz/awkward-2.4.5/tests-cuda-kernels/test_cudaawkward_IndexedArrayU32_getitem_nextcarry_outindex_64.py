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

def test_cuda_awkward_IndexedArrayU32_getitem_nextcarry_outindex_64_1():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toindex = cupy.array([123, 123, 123], dtype=cupy.uint32)
    fromindex = cupy.array([1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1], dtype=cupy.uint32)
    lenindex = 3
    lencontent = 2
    funcC = cupy_backend['awkward_IndexedArray_getitem_nextcarry_outindex', cupy.int64, cupy.uint32, cupy.uint32]
    funcC(tocarry, toindex, fromindex, lenindex, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 0, 0]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toindex = [0.0, 1.0, 2.0]
    assert cupy.array_equal(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

def test_cuda_awkward_IndexedArrayU32_getitem_nextcarry_outindex_64_2():
    tocarry = cupy.array([123], dtype=cupy.int64)
    toindex = cupy.array([123], dtype=cupy.uint32)
    fromindex = cupy.array([1, 4, 2, 3, 1, 2, 3, 1, 4, 3, 2, 1, 3, 2, 4, 5, 1, 2, 3, 4, 5], dtype=cupy.uint32)
    lenindex = 3
    lencontent = 2
    funcC = cupy_backend['awkward_IndexedArray_getitem_nextcarry_outindex', cupy.int64, cupy.uint32, cupy.uint32]

def test_cuda_awkward_IndexedArrayU32_getitem_nextcarry_outindex_64_3():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    toindex = cupy.array([123, 123, 123], dtype=cupy.uint32)
    fromindex = cupy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.uint32)
    lenindex = 3
    lencontent = 5
    funcC = cupy_backend['awkward_IndexedArray_getitem_nextcarry_outindex', cupy.int64, cupy.uint32, cupy.uint32]
    funcC(tocarry, toindex, fromindex, lenindex, lencontent)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_toindex = [0.0, 1.0, 2.0]
    assert cupy.array_equal(toindex[:len(pytest_toindex)], cupy.array(pytest_toindex))

