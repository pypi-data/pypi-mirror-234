from no_global_nonlocal_vars import no_global_nonlocal_vars
import numpy as np
import pytest


def test_no_global_nonlocal_vars_BASIC():
    # Create "global" variable that should not be used
    x = 0
    repeat = 1

    # Correct Output
    @no_global_nonlocal_vars
    def no_global_nonlocal_vars_BASIC(x, repeat):
        return np.array([x] * repeat)

    assert np.all(
        no_global_nonlocal_vars_BASIC(x=4, repeat=5) == np.array([4, 4, 4, 4, 4])
    )


def test_no_global_nonlocal_vars_ARGTYPO():
    # Create "global" variable that should not be used
    x = 0
    repeat = 1

    # Error from typo
    @no_global_nonlocal_vars
    def no_global_nonlocal_vars_ARGTYPO(x_typo, repeat_typo):
        return np.array([x] * repeat)

    with pytest.raises(AssertionError):
        output = no_global_nonlocal_vars_ARGTYPO(4, 5)


def test_no_global_nonlocal_vars_NESTED():
    # Create "global" variable that should not be used
    x = 0
    repeat = 1

    # Nested function works
    @no_global_nonlocal_vars
    def no_global_nonlocal_vars_NESTED(x, repeat=10):
        @no_global_nonlocal_vars
        def helper(x, repeat):
            return np.array([x] * repeat)

        return helper(x, repeat)

    assert np.all(no_global_nonlocal_vars_NESTED(x=2, repeat=3) == np.array([2, 2, 2]))


def test_no_global_nonlocal_vars_NESTED_ARGTYPO():
    # Create "global" variable that should not be used
    x = 0
    repeat = 1

    # Error from nested function typo
    @no_global_nonlocal_vars
    def no_global_nonlocal_vars_NESTED_ARGTYPO(x, repeat=10):
        @no_global_nonlocal_vars
        def helper(x_typo, repeat_typo):
            return np.array([x] * repeat)

        return helper(x, repeat)

    with pytest.raises(AssertionError):
        output = no_global_nonlocal_vars_NESTED_ARGTYPO(2, 3)
