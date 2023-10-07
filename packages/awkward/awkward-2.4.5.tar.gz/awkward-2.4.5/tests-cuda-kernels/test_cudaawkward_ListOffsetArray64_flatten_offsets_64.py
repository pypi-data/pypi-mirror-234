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

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_1():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_2():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [3, 3, 3]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_3():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_4():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_5():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_6():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_7():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [3, 4, 4]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_8():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 1, 1]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_9():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 3, 3]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_10():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_11():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_12():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [3, 3, 2]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_13():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 1, 2]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_14():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 0, 1]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_15():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_16():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_17():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [3, 2, 3]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_18():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 2, 0]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_19():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 1, 2]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_20():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_21():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_22():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 2, 2]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_23():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [2, 2, 2]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_24():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [1, 1, 1]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

def test_cuda_awkward_ListOffsetArray64_flatten_offsets_64_25():
    tooffsets = cupy.array([123, 123, 123], dtype=cupy.int64)
    outeroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    outeroffsetslen = 3
    inneroffsets = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    inneroffsetslen = 3
    funcC = cupy_backend['awkward_ListOffsetArray_flatten_offsets', cupy.int64, cupy.int64, cupy.int64]
    funcC(tooffsets, outeroffsets, outeroffsetslen, inneroffsets, inneroffsetslen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tooffsets = [0, 0, 0]
    assert cupy.array_equal(tooffsets[:len(pytest_tooffsets)], cupy.array(pytest_tooffsets))

