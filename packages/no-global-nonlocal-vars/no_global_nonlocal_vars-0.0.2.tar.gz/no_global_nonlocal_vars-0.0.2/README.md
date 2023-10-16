# no_global_nonlocal_vars

Function decorator that ensures that no global and no nonlocal variables are used, making Jupyter notebooks much safer

# Installing

Install:
```
pip install no_global_nonlocal_vars
```

# Usage

```
# Correct Output
@no_global_nonlocal_vars
def test_no_global_nonlocal_vars_GOOD(x, repeat):
    return np.array([x] * repeat)


# Error from typo
@no_global_nonlocal_vars
def test_no_global_nonlocal_vars_typo_GOOD(x_typo, repeat_typo):
    return np.array([x] * repeat)


# Nested function works
@no_global_nonlocal_vars
def test_no_global_nonlocal_vars_nested_GOOD(x, repeat=10):

    @no_global_nonlocal_vars
    def helper(x, repeat):
        return np.array([x] * repeat)

    return helper(x, repeat)


# Error from nonlocal variable typo
@no_global_nonlocal_vars
def test_no_global_nonlocal_vars_nested_typo_GOOD(x, repeat=10):

    @no_global_nonlocal_vars
    def helper(x_typo, repeat_typo):
        return np.array([x] * repeat)

    return helper(x, repeat)
```

# Notes

* The errors show up only upon first time running the function, not at function definition time

# Related Work

* https://github.com/tillahoffmann/localscope

* https://github.com/diazona/localscope
