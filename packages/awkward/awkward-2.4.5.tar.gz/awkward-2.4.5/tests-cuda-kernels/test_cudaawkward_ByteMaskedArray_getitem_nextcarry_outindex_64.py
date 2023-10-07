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

def test_cuda_awkward_ByteMaskedArray_getitem_nextcarry_outindex_64_1():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    outindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    mask = cupy.array([1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_getitem_nextcarry_outindex', cupy.int64, cupy.int64, cupy.int8]
    funcC(tocarry, outindex, mask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 2]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_outindex = [0.0, 1.0, 2.0]
    assert cupy.array_equal(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cuda_awkward_ByteMaskedArray_getitem_nextcarry_outindex_64_2():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    outindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    mask = cupy.array([0, 0, 0, 0, 0], dtype=cupy.int8)
    length = 3
    validwhen = False
    funcC = cupy_backend['awkward_ByteMaskedArray_getitem_nextcarry_outindex', cupy.int64, cupy.int64, cupy.int8]
    funcC(tocarry, outindex, mask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 2]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_outindex = [0.0, 1.0, 2.0]
    assert cupy.array_equal(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cuda_awkward_ByteMaskedArray_getitem_nextcarry_outindex_64_3():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    outindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    mask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_getitem_nextcarry_outindex', cupy.int64, cupy.int64, cupy.int8]
    funcC(tocarry, outindex, mask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 2]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_outindex = [0.0, 1.0, 2.0]
    assert cupy.array_equal(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

def test_cuda_awkward_ByteMaskedArray_getitem_nextcarry_outindex_64_4():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    outindex = cupy.array([123, 123, 123], dtype=cupy.int64)
    mask = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int8)
    length = 3
    validwhen = True
    funcC = cupy_backend['awkward_ByteMaskedArray_getitem_nextcarry_outindex', cupy.int64, cupy.int64, cupy.int8]
    funcC(tocarry, outindex, mask, length, validwhen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 2]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))
    pytest_outindex = [0.0, 1.0, 2.0]
    assert cupy.array_equal(outindex[:len(pytest_outindex)], cupy.array(pytest_outindex))

