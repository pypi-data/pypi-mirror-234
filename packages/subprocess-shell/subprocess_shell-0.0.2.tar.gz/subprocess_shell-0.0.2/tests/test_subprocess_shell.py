import subprocess_shell
from subprocess_shell import *
import hypothesis
import hypothesis.strategies as h_strategies
import pytest
import itertools
import re
import subprocess
import sys
import tempfile
import time
import typing


DATETIME_PATTERN = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{6})?"
CODE_PATTERN = r"(\?|\d+)"


_v_ = (
    "import sys; stdin = sys.stdin.read(); print('stdout', stdin);"
    " print('stderr', stdin, file=sys.stderr)"
)
I_ARGUMENTS = [sys.executable, "-c", _v_]

I_STDOUT_PATTERN = lambda datetime_name, stdin_pattern, code_pattern=CODE_PATTERN: rf"""
`{re.escape(subprocess.list2cmdline(I_ARGUMENTS))}` \((?P<{datetime_name}>{DATETIME_PATTERN}), {code_pattern}\)
\+\|stdout {stdin_pattern}
\+\|

"""[1:-1]
I_STDERR_PATTERN = lambda datetime_name, stdin_pattern, code_pattern=CODE_PATTERN: rf"""
`{re.escape(subprocess.list2cmdline(I_ARGUMENTS))}` \((?P<{datetime_name}>{DATETIME_PATTERN}), {code_pattern}\)
-\|stderr {stdin_pattern}
-\|

"""[1:-1]


def test_1_trivial(capsys):
    assert ["sleep", "0"] >> start() >> wait() == 0
    _assert("", "", capsys)


def test_1_wait(capsys):
    for stdout, stderr in itertools.product([False, True], [False, True]):
        assert I_ARGUMENTS >> start() >> wait(stdout=stdout, stderr=stderr) == 0

        _v_ = I_STDOUT_PATTERN("d1", "") if stdout else ""
        groups = _assert(_v_, I_STDERR_PATTERN("d2", "") if stderr else "", capsys)

        assert not (stdout and stderr and groups["d1"] != groups["d2"])


def test_1_io(capsys):
    _v_ = itertools.product([False, True], [False, True], [False, True])
    for stdout, stderr, bytes in _v_:
        stdout_object = b"stdout this\n" if bytes else "stdout this\n"
        stderr_object = b"stderr this\n" if bytes else "stderr this\n"

        _v_ = {
            (False, False): None,
            (True, False): stdout_object,
            (False, True): stderr_object,
            (True, True): (stdout_object, stderr_object),
        }
        _v_ = typing.cast(dict[tuple[bool, bool], typing.Any], _v_)[(stdout, stderr)]
        expected = _v_

        _v_ = read(stdout=stdout, stderr=stderr, bytes=bytes)
        assert (I_ARGUMENTS >> start() >> write("this") >> _v_) == expected

        _v_ = "" if stdout else I_STDOUT_PATTERN("d1", "this")
        groups = _assert(_v_, "" if stderr else I_STDERR_PATTERN("d2", "this"), capsys)

        assert not (not stdout and not stderr and groups["d1"] != groups["d2"])


def test_1_file(capsys):
    with tempfile.NamedTemporaryFile() as stdout_file, tempfile.NamedTemporaryFile() as stderr_file:
        _v_ = I_ARGUMENTS >> start(stdout=stdout_file.name, stderr=stderr_file.name)
        assert _v_ >> wait() == 0

        _assert("", "", capsys)
        assert stdout_file.read() == b"stdout \n"
        assert stderr_file.read() == b"stderr \n"


def test_1_function(capsys):
    stdout_list = [b""]
    stderr_list = [b""]

    _v_ = I_ARGUMENTS >> start(stdout=stdout_list.append, stderr=stderr_list.append)
    assert _v_ >> wait() == 0

    for _ in range(10):
        if stdout_list[-1] is None and stderr_list[-1] is None:
            break

        time.sleep(0.01)

    else:
        raise Exception

    _assert("", "", capsys)
    assert b"".join(stdout_list[:-1]) == b"stdout \n"
    assert b"".join(stderr_list[:-1]) == b"stderr \n"


def test_1_fail(capsys):
    arguments = [sys.executable, "-c", "raise SystemExit(1)"]

    assert arguments >> start() >> wait(return_codes=None) == 1
    _assert("", "", capsys)

    _v_ = re.escape(subprocess.list2cmdline(arguments))
    _v_ = rf"`{_v_}` \({DATETIME_PATTERN}, 1\)"
    with pytest.raises(subprocess_shell.ProcessFailedError, match=_v_):
        assert arguments >> start() >> wait(return_codes=(0,)) == 0

    _assert("", "", capsys)

    assert arguments >> start() >> wait(return_codes=(1,)) == 1
    _assert("", "", capsys)


def test_2_trivial(capsys):
    assert ["echo", "this"] >> start() + ["cat", "-"] >> start() >> wait() == 0

    _v_ = rf"""
`cat -` \({DATETIME_PATTERN}, {CODE_PATTERN}\)
\+\|this
\+\|

"""[1:-1]
    _assert(_v_, "", capsys)


def test_2_wait(capsys):
    for stdout, stderr in itertools.product([False, True], [False, True]):
        _v_ = I_ARGUMENTS >> start() + I_ARGUMENTS >> start()
        assert _v_ >> wait(stdout=stdout, stderr=stderr) == 0

        groups = _assert(
            rf"""
`{re.escape(subprocess.list2cmdline(I_ARGUMENTS))}` \((?P<d1>{DATETIME_PATTERN}), {CODE_PATTERN}\)
\+\|stdout stdout 
\+\|
\+\|

"""[1:-1] if stdout else "",
            I_STDERR_PATTERN("d0", "") + (rf"""
`{re.escape(subprocess.list2cmdline(I_ARGUMENTS))}` \((?P<d2>{DATETIME_PATTERN}), {CODE_PATTERN}\)
-\|stderr stdout 
-\|
-\|

"""[1:-1] if stderr else ""),
            capsys,
        )

        _v_ = groups["d0"] != groups.get("d1") and groups["d0"] != groups.get("d2")
        assert _v_ and not (stdout and stderr and groups["d1"] != groups["d2"])

    for stdout, stderr in itertools.product([False, True], [False, True]):
        _v_ = I_ARGUMENTS >> start() - I_ARGUMENTS >> start()
        assert _v_ >> wait(stdout=stdout, stderr=stderr) == 0

        groups = _assert(
            I_STDOUT_PATTERN("d0", "") + (rf"""
`{re.escape(subprocess.list2cmdline(I_ARGUMENTS))}` \((?P<d1>{DATETIME_PATTERN}), {CODE_PATTERN}\)
\+\|stdout stderr 
\+\|
\+\|

"""[1:-1] if stdout else ""),
            rf"""
`{re.escape(subprocess.list2cmdline(I_ARGUMENTS))}` \((?P<d2>{DATETIME_PATTERN}), {CODE_PATTERN}\)
-\|stderr stderr 
-\|
-\|

"""[1:-1] if stderr else "",
            capsys,
        )

        _v_ = groups["d0"] != groups.get("d1") and groups["d0"] != groups.get("d2")
        assert _v_ and not (stdout and stderr and groups["d1"] != groups["d2"])


def test_2_fail():
    source_arguments = ["echo", "this"]
    target_arguments = ["cat", "-"]
    fail_arguments = [sys.executable, "-c", "raise SystemExit(1)"]

    _v_ = (
        rf"^`{re.escape(subprocess.list2cmdline(fail_arguments))}`"
        rf" \({DATETIME_PATTERN}, 1\) \+"
        rf" `{re.escape(subprocess.list2cmdline(target_arguments))}`"
        rf" \({DATETIME_PATTERN}, {CODE_PATTERN}\)$"
    )
    with pytest.raises(subprocess_shell.ProcessFailedError, match=_v_):
        _ = fail_arguments >> start() + target_arguments >> start() >> wait()

    _v_ = (
        rf"^`{re.escape(subprocess.list2cmdline(source_arguments))}`"
        rf" \({DATETIME_PATTERN}, {CODE_PATTERN}\) \+"
        rf" `{re.escape(subprocess.list2cmdline(fail_arguments))}`"
        rf" \({DATETIME_PATTERN}, 1\)$"
    )
    with pytest.raises(subprocess_shell.ProcessFailedError, match=_v_):
        _ = source_arguments >> start() + fail_arguments >> start() >> wait()

    _v_ = (
        rf"^`{re.escape(subprocess.list2cmdline(fail_arguments))}`"
        rf" \({DATETIME_PATTERN}, 1\) \+"
        rf" `{re.escape(subprocess.list2cmdline(fail_arguments))}`"
        rf" \({DATETIME_PATTERN}, {CODE_PATTERN}\)$"
    )
    with pytest.raises(subprocess_shell.ProcessFailedError, match=_v_):
        _ = fail_arguments >> start() + fail_arguments >> start() >> wait()


def test_codec(capsys):
    for text, bytes in itertools.product([False, True], [False, True]):
        _v_ = b"this\n" if bytes else "this\n"
        assert ["echo", "this"] >> start(text=text) >> read(bytes=bytes) == _v_

        _assert("", "", capsys)


_v_ = h_strategies.sampled_from(["\n", None])
_v_ = h_strategies.one_of(h_strategies.text(max_size=5), _v_)
_v_ = h_strategies.lists(_v_, max_size=5)


@hypothesis.settings(
    suppress_health_check=[hypothesis.HealthCheck.function_scoped_fixture]
)
@hypothesis.given(objects=_v_, bufsize=h_strategies.sampled_from([0, 2, 3, 4, 5]))
def test_lines(objects, bufsize, capsys):
    capsys.readouterr()

    _v_ = "".join(filter(lambda object: isinstance(object, str), objects))
    expected_lines = re.split(r"(?<=\n)", _v_)

    if expected_lines[-1] == "":
        expected_lines.pop()

    process = [sys.executable] >> start(bufsize=bufsize) >> write(f"""
import sys

objects = {repr(objects)}
for object in objects:
    if isinstance(object, str):
        sys.stdout.write(object)
    elif object is None:
        sys.stdout.flush()
    else:
        raise Exception
""")
    typing.cast(typing.IO, process.get_subprocess().stdin).close()
    assert list(process.get_stdout_lines()) == expected_lines
    assert process >> wait() == 0
    _assert("", "", capsys)


def _assert(stdout_pattern, stderr_pattern, capsys):
    capture_result = capsys.readouterr()

    stdout_match = re.search(rf"\A{stdout_pattern}\Z", capture_result.out, re.MULTILINE)
    if stdout_match is None:
        raise Exception(f"\n{capture_result.out}")

    stderr_match = re.search(rf"\A{stderr_pattern}\Z", capture_result.err, re.MULTILINE)
    if stderr_match is None:
        raise Exception(f"\n{capture_result.err}")

    return stdout_match.groupdict() | stderr_match.groupdict()
