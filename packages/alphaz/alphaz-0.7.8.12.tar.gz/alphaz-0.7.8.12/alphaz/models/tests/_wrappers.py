# MODULES
from typing import Callable, Any
from pathlib import Path

# LOCALS
from ...apis.users.users import try_su_login, logout_su
from ..main import AlphaException
from ...models.tests import AlphaTest
from ...libs import dict_lib

from ._levels import Levels
from ._save import AlphaSave

from core import core

LOG = core.get_logger("tests")

TEST_METHOD_NAME = "test_alpha_in"


def call_function(
    fct: Callable,
    obj: object,
    args: list | None = None,
    kwargs: dict[str, object] | None = None,
) -> Any:
    """
    Call a function with arguments and return its output.

    Args:
        fct: The function to call.
        obj: The object to pass as the first argument if the function is a method.
        args: A list of positional arguments to pass to the function.
        kwargs: A dictionary of keyword arguments to pass to the function.

    Returns:
        The output of the function.
    """
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}
    if obj is not None and hasattr(fct, "__self__"):
        # If the function is a method, pass obj as the first argument.
        return fct(obj, *args, **kwargs)
    else:
        # Otherwise, call the function directly.
        return fct(*args, **kwargs)


def test(
    mandatory: bool = False,
    save: bool = False,
    save_ext: str = ".ast",
    save_path: Path | None = None,
    begin: Callable | None = None,
    end: Callable | None = None,
    save_post_process: Callable | None = None,
    return_diff: bool = False,
    begin_args: list | None = None,
    begin_kwargs: dict[str, Any] | None = None,
    end_args: list | None = None,
    end_kwargs: dict[str, Any] | None = None,
    description: str | None = None,
    stop: bool = True,
    disable: bool = False,
    level: Levels = Levels.MEDIUM,
    admin_user_id: str | None = None,
    admin_user_name: str | None = None,
) -> Callable:
    """
    Decorator used to mark a test function to be run.

    The test function should be a method of a class which inherits from `unittest.TestCase`.
    The decorator wraps the function in another function which performs various pre- and post-processing.

    Args:
        mandatory: Whether this test is mandatory for the test suite to pass.
        save: Whether to save the output of the test for future runs.
        begin: A function to be run before the test function is run.
        end: A function to be run after the test function is run.
        begin_args: A list of arguments to pass to the begin function.
        begin_kwargs: A dictionary of keyword arguments to pass to the begin function.
        end_args: A list of arguments to pass to the end function.
        end_kwargs: A dictionary of keyword arguments to pass to the end function.
        description: A description of the test.
        stop: Whether to stop running the test suite if this test fails.
        disable: Whether to disable the test.
        level: The level of the test.
        admin_user_id: The ID of the admin user to use to run the test.
        admin_user_name: The name of the admin user to use to run the test.

    Returns:
        A wrapper function which performs pre- and post-processing before and after running the test function.
    """

    def test_alpha_in(func: Callable) -> Callable:
        def test_wrapper(*args, **kwargs):
            if len(args) == 0:
                return
            TestClass: AlphaTest = args[0]
            TestClass.output = None

            logged_output = None
            if admin_user_id is not None or admin_user_name is not None:
                logged_output = try_su_login(
                    admin_user_id if admin_user_id is not None else admin_user_name
                )
                if logged_output is None:
                    raise AlphaException("Unable to auth as an admin")

            if begin:
                call_function(begin, TestClass, begin_args, begin_kwargs)

            try:
                output = func(*args, **kwargs)

                if save:
                    alpha_save = AlphaSave(root=save_path, ext=save_ext)
                    return_save = alpha_save.load(
                        filename=func.__name__,
                        class_name=TestClass.__class__.__name__,
                    )

                    alpha_save.save(
                        object_to_save=output,
                        filename=func.__name__,
                        class_name=TestClass.__class__.__name__,
                    )

                    return_save = (
                        save_post_process(output, return_save)
                        if save_post_process is not None
                        else return_save
                    )

                    if return_diff:
                        TestClass.outputs["dicts_diff"] = dict_lib.get_dicts_diff(
                            dict_1=output, dict_2=return_save
                        )

                    TestClass.assert_equal(return_save, output)
            except Exception as ex:
                TestClass.output = False
                LOG.error(
                    message=f"An exception occurred with {TestClass.__class__.__name__}.{func.__name__}. The test has been marked as failed.",
                    ex=ex,
                )

            if end:
                call_function(end, TestClass, end_args, end_kwargs)

            if logged_output is not None:
                logout_su()

            if TestClass.output is not None:
                # When using assertions
                TestClass.outputs[func.__name__] = TestClass.output
                return TestClass.output
            else:
                # output is not None only when using return
                TestClass.outputs[func.__name__] = output
                return output

        if hasattr(func, "__name__"):
            test_wrapper.__name__ = func.__name__
            parameters = {
                "save": save,
                "description": description,
                "stop": stop,
                "disable": disable,
                "level": level,
                "func": func,
            }
            test_wrapper.__dict__ = parameters
        else:
            pass

        return test_wrapper

    return test_alpha_in


def save_test(func: Callable) -> Callable:
    """
    Decorator to save the return value of a function and compare it with the next call.

    Usage:
        @save
        def my_func(arg1, arg2):
            return arg1 + arg2

        # First call
        result1 = my_func(1, 2)
        assert result1 == 3

        # Second call, returns True because the result is the same
        result2 = my_func(1, 2)
        assert result2 is True

    Args:
        func: The function to decorate.

    Returns:
        The decorated function.
    """

    def save_method_result(*args, **kwargs):
        get_return, get_name = False, False
        new_kwargs = {}
        args = list(args)

        for kw in kwargs.keys():
            if kw == "get_return":
                get_return = True
            elif kw == "get_name":
                get_name = True
            else:
                new_kwargs[kw] = kwargs[kw]

        return_save = AlphaSave.load(func.__name__)

        if get_return:
            return func(*args, **new_kwargs)
        elif get_name:
            return func.__name__
        else:
            return func(*args, **new_kwargs) == return_save

    return save_method_result
