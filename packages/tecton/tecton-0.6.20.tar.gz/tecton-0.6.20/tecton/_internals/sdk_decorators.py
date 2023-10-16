import inspect
import threading
from functools import wraps
from typing import Callable
from typing import Optional

import pendulum
from typeguard import typechecked

from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals.analytics import AnalyticsLogger
from tecton._internals.metadata_service_impl import trace as metadata_service_trace
from tecton.framework import validation_mode
from tecton_core import conf
from tecton_core.errors import TectonAPIInaccessibleError
from tecton_core.errors import TectonAPIValidationError
from tecton_core.errors import TectonInternalError
from tecton_core.id_helper import IdHelper


analytics = AnalyticsLogger()
thread_local_data = threading.local()
sdk_public_method_decorator_enabled = True


def disable_sdk_public_method_decorator():
    global sdk_public_method_decorator_enabled
    sdk_public_method_decorator_enabled = False


def documented_by(func):
    """Normally you should just use functools.wraps over this, but wraps() doesn't work nicely
    when you try to wrap a classmethod in a normal func.
    """

    def wrapper(target):
        target.__doc__ = func.__doc__
        return target

    return wrapper


def assert_valid(func):
    """Check if the object has been validated, if not throw an error.

    This should only be used for private methods, as opposed to public methods, which should use
    @sdk_public_method(requires_validation=True) and will trigger automatic validation if needed.
    """

    @wraps(func)
    def wrapper(fco_object, *args, **kwargs):
        if not fco_object._is_valid:
            raise errors.TECTON_OBJECT_REQUIRES_VALIDATION(
                func.__name__, type(fco_object).__name__, fco_object.info.name
            )
        return func(fco_object, *args, **kwargs)

    return wrapper


def assert_remote_object(
    original_function: Optional[Callable] = None,
    *,
    error_message: Callable[[str], Exception] = errors.INVALID_USAGE_FOR_LOCAL_TECTON_OBJECT,
):
    """Assert this function is being called on a remote Tecton object, aka an object applied and fetched from the backend, and raise error otherwise.

    :param: error_message: error message to raise if the Tecton object is locally defined. The error_message param must contain a function that takes
    in the target function's name as a param and returns an Exception.
    """

    def inner_decorater(target):
        @wraps(target)
        def wrapper(fco_object, *args, **kwargs):
            if fco_object.info._is_local_object:
                raise error_message(target.__name__)
            return target(fco_object, *args, **kwargs)

        return wrapper

    if original_function:
        return inner_decorater(original_function)

    return inner_decorater


def assert_local_object(
    original_function: Optional[Callable] = None,
    *,
    error_message: Callable[[str], Exception] = errors.INVALID_USAGE_FOR_REMOTE_TECTON_OBJECT,
):
    """Assert this function is being called on a local Tecton object, aka an object created locally (as opposed to being fetched from the backend).

    :param: error_message: error message to raise if the Tecton object is not locally defined. The error_message param must contain a function that takes
    in the target function's name as a param and returns an Exception.
    """

    def inner_decorater(target):
        @wraps(target)
        def wrapper(fco_object, *args, **kwargs):
            if not fco_object.info._is_local_object:
                raise error_message(target.__name__)
            return target(fco_object, *args, **kwargs)

        return wrapper

    if original_function:
        return inner_decorater(original_function)

    return inner_decorater


def sdk_public_method(
    original_function: Optional[Callable] = None,
    *,
    requires_validation: bool = False,
    validation_error_message: Callable[[str, str, str], Exception] = errors.TECTON_OBJECT_REQUIRES_VALIDATION,
):
    """Decorator for public SDK methods that should be have analytics logging.

    :param original_function: The function to be wrapped.
    :param requires_validation: If True, will run Tecton object validation (if needed) before entering running original
        function. Automatically triggered validation will be logged separately. Should only be set to True when used
        to wrap a "Tecton object" (e.g. a DataSource or FeatureView) method.
    :param validation_error_message: The error message function to use if the object has not been validated and
        automatic validation is not enabled.
    """

    def inner_decorator(target_func):
        arg_names = _get_arg_names(target_func)

        @wraps(target_func)
        def _sdk_public_method_wrapper(*args, **kwargs):
            if requires_validation:
                if not _is_method(target_func) or not hasattr(args[0], "_is_valid"):
                    raise TectonInternalError(
                        "sdk_public_method(requires_validation=True) should only be used with Tecton object methods."
                    )
                fco_object = args[0]
                # Object has not been validated yet.
                if not fco_object._is_valid:
                    if conf.get_or_none("TECTON_VALIDATION_MODE") == validation_mode.ValidationMode.AUTOMATIC:
                        fco_object._run_automatic_validation()
                    else:
                        raise validation_error_message(
                            target_func.__name__, type(fco_object).__name__, fco_object.info.name
                        )

            if not sdk_public_method_decorator_enabled:
                return target_func(*args, **kwargs)

            if not hasattr(thread_local_data, "in_tecton_sdk_public_method_wrapper"):
                thread_local_data.in_tecton_sdk_public_method_wrapper = False

            already_in_wrapper = thread_local_data.in_tecton_sdk_public_method_wrapper
            if already_in_wrapper:
                return target_func(*args, **kwargs)

            try:
                thread_local_data.in_tecton_sdk_public_method_wrapper = True
                return _invoke_and_transform_errors(
                    target_func, args, kwargs, arg_names, analytics is not None, not already_in_wrapper, typecheck=True
                )
            finally:
                thread_local_data.in_tecton_sdk_public_method_wrapper = already_in_wrapper

        return _sdk_public_method_wrapper

    if original_function:
        return inner_decorator(original_function)

    return inner_decorator


def _is_method(func):
    params = inspect.signature(func).parameters
    return "self" in params or "cls" in params


def _get_arg_names(func):
    arg_names = []
    for i, param in enumerate(inspect.signature(func).parameters.values()):
        name = param.name
        if i == 0 and _is_method(func):
            continue
        arg_names.append(name)
    return arg_names


def _invoke_and_transform_errors(
    func, args, kwargs, arg_names, log_analytics: bool, is_top_level: bool, typecheck: bool = False
):
    if typecheck:
        func = typechecked(func)

    if _is_method(func):
        method_object = args[0]
        method_args = args[1:]
    else:
        method_object = None
        method_args = args

    trace_id = IdHelper.generate_string_id()

    if log_analytics:
        start_time = pendulum.now("UTC")
        analytics.log_method_entry(trace_id, method_object, func, method_args, kwargs, arg_names)

    metadata_service_trace.set_trace_id(trace_id)
    return_value = None

    try:
        return_value = func(*args, **kwargs)
        caught_exception = None
        return return_value
    except TectonAPIValidationError as e:
        caught_exception = e
        raise errors.VALIDATION_ERROR_FROM_MDS(str(e), trace_id)
    except TectonAPIInaccessibleError as e:
        caught_exception = e
        raise errors.MDS_INACCESSIBLE(metadata_service._get_host_port())
    except Exception as e:
        caught_exception = e
        # Do not chain the exception, just let it pass through. This leads to more legible stack traces and errors.
        raise
    finally:
        metadata_service_trace.set_trace_id(None)
        if log_analytics:
            end_time = pendulum.now("UTC")
            execution_time = end_time - start_time
            analytics.log_method_return(trace_id, method_object, func, return_value, execution_time, caught_exception)
