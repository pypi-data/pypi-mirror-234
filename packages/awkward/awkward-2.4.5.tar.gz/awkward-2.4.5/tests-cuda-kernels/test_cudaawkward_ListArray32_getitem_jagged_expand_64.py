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

def test_cuda_awkward_ListArray32_getitem_jagged_expand_64_1():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    jaggedsize = 1
    length = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int32, cupy.int32]
    funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [1, 1, 1]
    assert cupy.array_equal(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [1, 1, 1]
    assert cupy.array_equal(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))
    pytest_tocarry = [0, 0, 0]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_ListArray32_getitem_jagged_expand_64_2():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    jaggedsize = 1
    length = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int32, cupy.int32]
    funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [2, 2, 2]
    assert cupy.array_equal(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [3, 3, 3]
    assert cupy.array_equal(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))
    pytest_tocarry = [0, 0, 0]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_ListArray32_getitem_jagged_expand_64_3():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    jaggedsize = 1
    length = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int32, cupy.int32]
    funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [2, 2, 2]
    assert cupy.array_equal(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [1, 1, 1]
    assert cupy.array_equal(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))
    pytest_tocarry = [0, 0, 0]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_ListArray32_getitem_jagged_expand_64_4():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    jaggedsize = 1
    length = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int32, cupy.int32]
    funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [1, 1, 1]
    assert cupy.array_equal(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [0, 0, 0]
    assert cupy.array_equal(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))
    pytest_tocarry = [0, 0, 0]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_ListArray32_getitem_jagged_expand_64_5():
    multistarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    multistops = cupy.array([123, 123, 123], dtype=cupy.int64)
    singleoffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromstarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int32)
    fromstops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int32)
    jaggedsize = 1
    length = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_expand', cupy.int64, cupy.int64, cupy.int64, cupy.int64, cupy.int32, cupy.int32]
    funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_multistarts = [0, 0, 0]
    assert cupy.array_equal(multistarts[:len(pytest_multistarts)], cupy.array(pytest_multistarts))
    pytest_multistops = [0, 0, 0]
    assert cupy.array_equal(multistops[:len(pytest_multistops)], cupy.array(pytest_multistops))
    pytest_tocarry = [0, 0, 0]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

