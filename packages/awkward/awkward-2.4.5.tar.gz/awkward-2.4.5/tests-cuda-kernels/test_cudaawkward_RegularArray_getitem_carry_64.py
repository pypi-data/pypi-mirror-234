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

def test_cuda_awkward_RegularArray_getitem_carry_64_1():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 4, 5, 3, 4, 5, 3, 4, 5]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_2():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 3, 2, 3, 2, 3]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_3():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 1, 1]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_4():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 3, 2, 3, 2, 3]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_5():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lencarry = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [6, 7, 8, 9, 10, 11, 9, 10, 11]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_6():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [4, 5, 6, 7, 6, 7]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_7():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lencarry = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 3, 3]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_8():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [4, 5, 6, 7, 6, 7]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_9():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [6, 7, 8, 3, 4, 5, 0, 1, 2]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_10():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [4, 5, 2, 3, 0, 1]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_11():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 1, 0]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_12():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [4, 5, 2, 3, 0, 1]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_13():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [3, 4, 5, 0, 1, 2, 6, 7, 8]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_14():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 3, 0, 1, 4, 5]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_15():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [1, 0, 2]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_16():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [2, 3, 0, 1, 4, 5]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_17():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 3
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_18():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 0, 1, 0, 1]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_19():
    tocarry = cupy.array([123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 1
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 0, 0]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

def test_cuda_awkward_RegularArray_getitem_carry_64_20():
    tocarry = cupy.array([123, 123, 123, 123, 123, 123], dtype=cupy.int64)
    fromcarry = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    lencarry = 3
    size = 2
    funcC = cupy_backend['awkward_RegularArray_getitem_carry', cupy.int64, cupy.int64]
    funcC(tocarry, fromcarry, lencarry, size)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tocarry = [0, 1, 0, 1, 0, 1]
    assert cupy.array_equal(tocarry[:len(pytest_tocarry)], cupy.array(pytest_tocarry))

