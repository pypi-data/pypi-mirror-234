"""Logging tools for flywheel-cli"""
import functools
import inspect
import logging

import wrapt

DEPRECATED_STACKLEVEL = 2  # warning stacklevel for deprecated decorator

# Define ANSI text color codes
ANSI_COLORS = {
    "black": "\x1b[38;5;0m",
    "maroon": "\x1b[38;5;1m",
    "green": "\x1b[38;5;2m",
    "olive": "\x1b[38;5;3m",
    "navy": "\x1b[38;5;4m",
    "purple": "\x1b[38;5;5m",
    "teal": "\x1b[38;5;6m",
    "silver": "\x1b[38;5;7m",
    "grey": "\x1b[38;5;8m",
    "red": "\x1b[38;5;9m",
    "orange": "\x1b[38;5;202m",
    "lime": "\x1b[38;5;10m",
    "yellow": "\x1b[38;5;11m",
    "blue": "\x1b[38;5;12m",
    "fuchsia": "\x1b[38;5;13",
    "aqua": "\x1b[38;5;14m",
    "white": "\x1b[38;5;15m",
}

# Define ANSI text format codes
ANSI_FORMAT = {"bold": "\x1b[1m", "underline": "\x1b[4m", "reverse": "\x1b[4m"}

# Define ANSI reset code to reset text formatting
ANSI_RESET = "\x1b[0m\n"

# Define console output format
LOG_FORMAT = "%(name)s (%(filename)s:%(lineno)d) %(levelname)s - %(message)s"


class ColorLogging(logging.Formatter):
    """
    A logging class to define colors used in printing of various messages. Parse
    this class into logging's StreamHandler()'s setFormatter method.

    Example:
        Enable color logging by parsing this class into setFormatter method

        .. code-block:: python
            # Configure logging
            log = logging.getLogger(__name__)
            log.setLevel(logging.DEBUG)
            # Create a console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            # Parse ColorLogging as an input
            console_handler.setFormatter(ColorLogging())  # parse class here
            log.addHandler(ch)

    Note:
        Colors used in this style can be altered by specifying them in the
        `LOGFORMAT` dictionary.
    """

    LOGFORMAT = {
        logging.DEBUG: ANSI_COLORS["grey"] + LOG_FORMAT + ANSI_RESET,
        logging.INFO: ANSI_COLORS["silver"] + LOG_FORMAT + ANSI_RESET,
        logging.WARNING: ANSI_COLORS["orange"] + LOG_FORMAT + ANSI_RESET,
        logging.ERROR: ANSI_COLORS["red"] + LOG_FORMAT + ANSI_RESET,
        logging.CRITICAL: ANSI_FORMAT["bold"]
        + ANSI_COLORS["red"]
        + LOG_FORMAT
        + ANSI_RESET,
    }

    def format(self, record):
        log_fmt = self.LOGFORMAT.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(ColorLogging())
log.addHandler(console_handler)


class DeprecatedAdapter(wrapt.AdapterFactory):
    """
    Deprecated decorator helper class to print complex messages. This class uses
    `wrapt` module to wrap an object and determine object type - function,
    class, methods, static method, or class method.

    Args:
        name (str, optional): Name to denote function being deprecated. Used to
            replace actual function name `foobar.__name__` with a a custom name.
        version (str, optional): Version number where a function was deprecated.
        message (str, optional): Optional message to print in
            DepreciationWarning for more information.

    Attributes:
        name (str): Name to denote function being deprecated.
        version (str): Version number where a function was deprecated.
        message (str): Optional message to print in DepreciationWarning.
    """

    def __init__(
        self,
        name: str = "",
        version: str = "",
        message: str = "",
    ):
        """
        Inits DepreciatedAdapter class. See docstring for
        `class DeprecatedAdapter`.
        """
        if not isinstance(name, str):
            raise TypeError(f"Entered name ({name}) is not a string.")
        if not isinstance(version, str):
            raise TypeError(f"Entered version ({version}) is not a string.")
        if not isinstance(message, str):
            raise TypeError(f"Entered message ({message}) is not a string.")
        self.name = name or ""
        self.version = version or ""
        self.message = message or ""
        super().__init__()

    def construct_msg(self, wrapped, instance):
        """
        Constructs deprication warning string.

        Args:
            wrapped (object): Wrapped function or class.
            instance (object): The object bounded to wrapped class.

        Returns:
            str: Warning message.
        """
        if not self.name:
            str_name = wrapped.__name__
        else:
            str_name = self.name
        fmt = "Call to "
        if instance is None:
            if inspect.isclass(wrapped):
                fmt += f"class {str_name} was deprecated"
            else:
                fmt += f"function {str_name} was deprecated"
        else:
            if inspect.isclass(instance):
                fmt += f"class method {str_name} was deprecated"
            else:
                fmt += f"method {str_name} was deprecated"
        if self.version:
            fmt += f" in CLI version {self.version}."
        else:
            fmt += "."
        if self.message:
            fmt += f" {self.message}"
        if not fmt.endswith("."):
            fmt += "."
        return fmt + "\n"

    def __call__(self, wrapped):
        """
        Decorates an input function or class

        Args:
            wrapped (object): Wrapped function or class.

        Returns
            object: Decorated function or class.
        """
        if inspect.isclass(wrapped):
            old_new1 = wrapped.__new__

            def wrapped_cls(cls, *args, **kwargs):
                msg = self.construct_msg(wrapped, None)
                log.warning(msg, stacklevel=DEPRECATED_STACKLEVEL)
                if old_new1 is object.__new__:
                    return old_new1(cls)
                # actually, we don't know the real signature of *old_new1*
                return old_new1(cls, *args, **kwargs)

            wrapped.__new__ = staticmethod(wrapped_cls)
        return wrapped


def deprecated(*args, **kwargs):
    """
    Decorator to mark functions or classes. Prints DeprecatedWarning based on
    input parameters.

    Example:
        Use the @deprecated decorater right before calling a function to mark it
        as deprecated.

        .. code-block:: python
            @deprecated
            def old_function(x, y):
                pass

        DeprecatedWarning messages can be customized with additional arguments.

        ..code-block:: python
            @deprecated(message="Use function foobar instead", version="1.2.3")
            def old_functon(x, y)
                pass

        The decorator can be applied to class or class method.

        .. code-block:: python
            class someClass:
                @deprecated
                def old_function(x, y):
                    pass

    Args:
        **name (str, optional): Name to denote function being deprecated. Used
            to replace actual function name `foobar.__name__` with a a custom
            name.
        **version (str, optional): Version number where a function was
            deprecated.
        **message (str, optional): Optional message to print in
            DepreciationWarning for more information.

    Returns:
        str: Prints custom warning.
    """
    if args and isinstance(args[0], str):
        kwargs["message"] = args[0]
        args = args[1:]

    if args and not callable(args[0]):
        raise TypeError(repr(type(args[0])))

    if args:
        adapter_cls = kwargs.pop("adapter_cls", DeprecatedAdapter)
        adapter = adapter_cls(**kwargs)

        wrapped = args[0]
        if inspect.isclass(wrapped):
            wrapped = adapter(wrapped)
            return wrapped

        elif inspect.isroutine(wrapped):

            @wrapt.decorator(adapter=adapter)
            def wrapper_function(wrapped_, instance_, args_, kwargs_):
                msg = adapter.construct_msg(wrapped_, instance_)
                log.warning(msg, stacklevel=DEPRECATED_STACKLEVEL)
                return wrapped_(*args_, **kwargs_)

            return wrapper_function(wrapped)

        else:
            raise TypeError(repr(type(wrapped)))

    return functools.partial(deprecated, **kwargs)
