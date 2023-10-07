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

def test_cuda_awkward_index_rpad_and_clip_axis1_64_1():
    tostarts = cupy.array([123, 123, 123], dtype=cupy.int64)
    tostops = cupy.array([123, 123, 123], dtype=cupy.int64)
    target = 3
    length = 3
    funcC = cupy_backend['awkward_index_rpad_and_clip_axis1', cupy.int64, cupy.int64]
    funcC(tostarts, tostops, target, length)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_tostarts = [0, 3, 6]
    assert cupy.array_equal(tostarts[:len(pytest_tostarts)], cupy.array(pytest_tostarts))
    pytest_tostops = [3, 6, 9]
    assert cupy.array_equal(tostops[:len(pytest_tostops)], cupy.array(pytest_tostops))

