import os
import sys
import traceback
from   pathlib      import Path


def ellipse(s: str, l: int = 92) -> str:
    """replace inner chars with ...  - and make it into single line"""
    s = repr(s)
    s = str(s)  # param s: str is only a hint - not enforced
    s = s.replace("\n", " ").replace("\r", " ")
    s = s.replace('\\n', " ")
    s = s.replace( '`', " ")
    s = s.strip()
    if len(s) <= l:
        return s
    halfLen = l // 2
    return f"{s[:halfLen]}...{s[-halfLen:]}"




def stackTrace(exc=None, lastX=2, printDirectly=True):
    """
        stackTrace() not part of the stacktrace
        traceback ends, where the exception *occurs*
    """

    if exc is None:
        exc = sys.exc_info()[1]

    cwd = os.getcwd()
    cwd = str(Path.cwd())

    lastX += 1  # dont show current helper func
    lastX += 2

    l = []

    extractedTrace = traceback.extract_tb(exc.__traceback__)
    # extractedTrace = list(reversed(extractedTrace[-lastX:]))
    extractedTrace = list(extractedTrace[-lastX:])

    lastFrames = extractedTrace[-lastX:]
    for idx1, frame in enumerate(lastFrames):
        line = f"\t{idx1:2d}: {frame.filename}:{frame.lineno} in {frame.name}"
        line = line.replace( cwd , "...")
        l.append( line )

    l.append( "\t-------")
    l.extend( traceback.format_exception_only(type(exc), exc) )

    s = "\n".join(l)

    if printDirectly:
        print(s)

    return s
