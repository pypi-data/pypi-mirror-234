import inspect
from typing import List


def inspect_caller(skip: int = 1,
                   return_info: List[str] = ('MODULE', 'FILENAME', 'CLASS', 'FUNC', 'LINENO')):
    """Get the name of a caller in the format module.class.method.

    :param skip: Specifies how many levels of stack to skip while getting caller name.
                 skip=1 means "who calls me"; skip=2 means "who calls my caller" etc.
    :param return_info: Caller info keys in returned dictionary: [MODULE | FILENAME | CLASS | FUNC | LINENO]
    :return: Caller info dictionary with keys specified in "return_info",
             while None return indicates empty "return_info" or "skip" exceeds stack height.
    """

    if not return_info:
        return None

    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return None

    caller_info = dict()
    parent_frame = stack[start][0]

    # package and module
    if 'MODULE' in return_info:
        module_info = inspect.getmodule(parent_frame)
        if module_info:
            caller_info['MODULE'] = module_info.__name__

    # caller filename
    if 'FILENAME' in return_info:
        caller_info['FILENAME'] = parent_frame.f_code.co_filename

    # class
    if 'CLASS' in return_info:
        klass = None
        if 'self' in parent_frame.f_locals:
            klass = parent_frame.f_locals['self'].__class__.__name__
        caller_info['CLASS'] = klass

    # method or function
    if 'FUNC' in return_info:
        func = None
        if parent_frame.f_code.co_name != '<module>':  # top level usually
            func = parent_frame.f_code.co_name
        caller_info['FUNC'] = func

    # line in caller
    if 'LINENO' in return_info:
        caller_info['LINENO'] = parent_frame.f_lineno

    # Remove reference to frame
    # See: https://docs.python.org/3/library/inspect.html#the-interpreter-stack
    del parent_frame

    return caller_info
