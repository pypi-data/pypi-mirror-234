import inspect


def is_variable(x):
    is_module = inspect.ismodule(x)
    is_class = inspect.isclass(x)
    is_function = inspect.isroutine(x)  # includes built-in and user-defined fns
    return not is_module and not is_class and not is_function


def no_global_nonlocal_vars(f):
    no_global_nonlocal_vars.already_passed_fns = set()

    def check_for_global_and_nonlocal_vars(*args, **kwargs):
        # Do not run this check again if f has already passed
        if f in no_global_nonlocal_vars.already_passed_fns:
            return f(*args, **kwargs)

        # Check for global and nonlocal variables
        closure_vars = inspect.getclosurevars(f)
        global_vars = {
            name: val
            for name, val in closure_vars.globals.items()
            if is_variable(val) and not name.startswith("__")
        }
        nonlocal_vars = {
            name: val
            for name, val in closure_vars.nonlocals.items()
            if is_variable(val) and not name.startswith("__")
        }

        # Assertions
        if len(global_vars) > 0:
            raise AssertionError(
                f"The function '{f.__name__}' should not be using the following global vars: {global_vars}"
            )
        if len(nonlocal_vars) > 0:
            raise AssertionError(
                f"The function '{f.__name__}' should not be using the following nonlocal vars: {nonlocal_vars}"
            )

        # Passed check
        no_global_nonlocal_vars.already_passed_fns.add(f)
        return f(*args, **kwargs)

    return check_for_global_and_nonlocal_vars
