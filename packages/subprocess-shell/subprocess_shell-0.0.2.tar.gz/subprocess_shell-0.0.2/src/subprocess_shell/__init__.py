"""
- start process: `{arguments} >> start(stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       pass_stdout=False,
                                       stderr=subprocess.PIPE,
                                       pass_stderr=False,
                                       queue_size=0,
                                       return_codes=(0,),
                                       **{kwargs})`
  - passes arguments to `subprocess.Popen`
  - by default, captures streams in queues
  - returns process
  - use `process.get_subprocess()` if necessary
- write to stdin: `{process} >> write({string or bytes})`
  - uses UTF-8 for en/decoding
  - writes and flushes
  - returns process
- wait for process: `{process} >> wait(stdout=True,
                                       stderr=True,
                                       return_codes=(0,))`
  - by default, prints stdout and stderr
  - by default, asserts return code
  - returns return code
- read streams: `{process} >> read(stdout=True,
                                   stderr=False,
                                   bytes=False,
                                   return_codes=(0,))`
  - waits for process
  - returns string or bytes or (string, string) or (bytes, bytes)
  - use `process.get_stdout_lines`, `process.get_stdout_strings`, `process.get_stdout_bytes`
    and `process.get_stderr_lines`, `process.get_stderr_strings`, `process.get_stderr_bytes`
    instead if necessary
- pass streams: `{process} + {arguments}` and `{process} - {arguments}`
  - e.g. `{arguments} >> start(return_codes=(0,)) + {arguments} >> start() >> wait()`
  - requires `start(pass_stdout=True)`, `start(pass_stderr=True)` unless directly adjacent to `+`, `-`
  - with `+`, passes stdout to stdin
  - with `-`, passes stderr to stdin
  - use `start(return_codes={return codes})` to assert return codes
"""

import collections.abc as c_abc
import datetime
import io
import os
import pathlib
import queue
import selectors
import subprocess
import sys
import threading
import typing


__all__ = ("start", "write", "wait", "read")


_BUFFER_SIZE = int(1e6)


def _read_streams():
    while True:
        for key, _ in _selector.select():
            while True:
                object = typing.cast(typing.IO, key.fileobj).read(_BUFFER_SIZE)
                if object in (None, b"", ""):
                    break

                key.data(object)

            if object in (b"", ""):
                _selector.unregister(key.fileobj)
                key.data(None)


_read_thread = threading.Thread(target=_read_streams, daemon=True)
_selector = selectors.DefaultSelector()


class _Start:
    def __init__(
        self,
        stdin: None | int | typing.IO = subprocess.PIPE,
        stdout: None
        | int
        | typing.IO
        | str
        | pathlib.Path
        | c_abc.Callable[[typing.AnyStr], typing.Any] = subprocess.PIPE,
        pass_stdout: bool = False,
        stderr: None
        | int
        | typing.IO
        | str
        | pathlib.Path
        | c_abc.Callable[[typing.AnyStr], typing.Any] = subprocess.PIPE,
        pass_stderr: bool = False,
        queue_size: int = 0,
        return_codes: c_abc.Container | None = (0,),
        **kwargs,
    ):
        super().__init__()

        self.stdin = stdin
        self.stdout = stdout
        self.pass_stdout = pass_stdout
        self.stderr = stderr
        self.pass_stderr = pass_stderr
        self.queue_size = queue_size
        self.return_codes = return_codes
        self.kwargs = kwargs

        assert not (pass_stdout and stdout not in (None, subprocess.PIPE))
        assert not (pass_stderr and stderr not in (None, subprocess.PIPE))

    def __rrshift__(self, object: typing.Union[c_abc.Iterable, "_Pass"]) -> "_Process":
        return _Process(object, self)

    def __add__(
        self, arguments: c_abc.Iterable
    ) -> "_PassStdout":  # `{arguments} >> start() + {arguments}`
        return _PassStdout(self, arguments)

    def __sub__(
        self, arguments: c_abc.Iterable
    ) -> "_PassStderr":  # `{arguments} >> start() - {arguments}`
        return _PassStderr(self, arguments)


start = _Start


class _Process:
    def __init__(self, object, start):
        super().__init__()

        self.object = object
        self.start = start

        if isinstance(object, _Pass):
            self._arguments = object.arguments
            self._source_process = object.process

            assert start.stdin in (None, subprocess.PIPE)
            stdin = (
                object.process._process.stderr
                if object.stderr
                else object.process._process.stdout
            )

        else:
            self._arguments = object
            self._source_process = None

            stdin = start.stdin

        self._stdout = self._get_argument(start.stdout)
        self._stderr = self._get_argument(start.stderr)
        self._start_datetime = datetime.datetime.now()

        _v_ = list(map(str, self._arguments))
        self._process = subprocess.Popen(
            _v_, stdin=stdin, stdout=self._stdout, stderr=self._stderr, **start.kwargs
        )

        self._stdout_queue = (
            None
            if self._process.stdout is None or start.pass_stdout
            else self._initialize_stream(self._process.stdout, start.stdout, start)
        )
        self._stderr_queue = (
            None
            if self._process.stderr is None or start.pass_stderr
            else self._initialize_stream(self._process.stderr, start.stderr, start)
        )

    def _get_argument(self, object):
        match object:
            case str() | pathlib.Path():
                object = open(object, "wb")

            case c_abc.Callable():
                object = subprocess.PIPE

        return object

    def _initialize_stream(self, stream, start_argument, start):
        if isinstance(start_argument, c_abc.Callable):
            queue_ = None
            function = start_argument

        else:
            queue_ = queue.Queue(maxsize=start.queue_size)
            function = queue_.put

        os.set_blocking(stream.fileno(), False)
        _selector.register(stream, selectors.EVENT_READ, data=function)

        if not _read_thread.is_alive():
            _read_thread.start()

        return queue_

    def get_stdout_lines(
        self, bytes: bool = False
    ) -> c_abc.Generator[typing.AnyStr, None, None]:
        return self._get_lines(self._stdout_queue, bytes)

    def get_stderr_lines(
        self, bytes: bool = False
    ) -> c_abc.Generator[typing.AnyStr, None, None]:
        return self._get_lines(self._stderr_queue, bytes)

    def _get_lines(self, queue, bytes) -> c_abc.Generator[typing.AnyStr, None, None]:
        objects: c_abc.Generator

        if bytes:
            objects = self._get_bytes(queue)
            newline_object = b"\n"
            empty_object = b""

        else:
            objects = self._get_strings(queue)
            newline_object = "\n"
            empty_object = ""

        parts = []

        for object in objects:
            start_index = 0
            while True:
                end_index = object.find(newline_object, start_index)
                if end_index == -1:
                    parts.append(object[start_index:])
                    break

                parts.append(object[start_index : end_index + 1])
                yield typing.cast(typing.AnyStr, empty_object.join(parts))
                parts.clear()

                start_index = end_index + 1

        object = empty_object.join(parts)
        if object != empty_object:
            yield typing.cast(typing.AnyStr, object)

    def get_stdout_strings(self) -> typing.Generator[str, None, None]:
        return self._get_strings(self._stdout_queue)

    def get_stderr_strings(self) -> typing.Generator[str, None, None]:
        return self._get_strings(self._stderr_queue)

    def _get_strings(self, queue):
        objects = iter(self._get_objects(queue))

        object = next(objects, None)
        if object is None:
            return

        if isinstance(object, str):
            yield object
            yield from objects

        else:
            yield object.decode()
            yield from (bytes.decode() for bytes in objects)

    def get_stdout_bytes(self) -> typing.Generator[bytes, None, None]:
        return self._get_bytes(self._stdout_queue)

    def get_stderr_bytes(self) -> typing.Generator[bytes, None, None]:
        return self._get_bytes(self._stderr_queue)

    def _get_bytes(self, queue):
        objects = iter(self._get_objects(queue))

        object = next(objects, None)
        if object is None:
            return

        if isinstance(object, str):
            yield object.encode()
            yield from (string.encode() for string in objects)

        else:
            yield object
            yield from objects

    def get_stdout_objects(self) -> typing.Generator[typing.AnyStr, None, None]:
        return self._get_objects(self._stdout_queue)

    def get_stderr_objects(self) -> typing.Generator[typing.AnyStr, None, None]:
        return self._get_objects(self._stderr_queue)

    def _get_objects(self, queue):
        assert queue is not None

        while True:
            object = queue.get()
            if object is None:
                queue.put(None)
                break

            yield object

    def __add__(self, arguments: c_abc.Iterable) -> "_Pass":
        assert self.start.pass_stdout
        return _Pass(self, False, arguments)

    def __sub__(self, arguments: c_abc.Iterable) -> "_Pass":
        assert self.start.pass_stderr
        return _Pass(self, True, arguments)

    def get_subprocess(self) -> subprocess.Popen:
        return self._process

    def get_source_process(self) -> typing.Union["_Process", None]:
        return self._source_process

    def get_chain_string(self) -> str:
        if self._source_process is None:
            pass_string = ""

        else:
            operator_string = "-" if self.object.stderr else "+"
            pass_string = f"{str(self._source_process)} {operator_string} "

        return f"{pass_string}{str(self)}"

    def __str__(self):
        self._process.poll()

        _v_ = "?" if self._process.returncode is None else self._process.returncode
        code_string = _v_

        _v_ = subprocess.list2cmdline(typing.cast(c_abc.Iterable, self._process.args))
        return f"`{_v_}` ({self._start_datetime.isoformat()}, {code_string})"


class _Pass:
    def __init__(self, process, stderr, arguments):
        super().__init__()

        self.process = process
        self.stderr = stderr
        self.arguments = arguments


class _Write:
    def __init__(self, object: typing.AnyStr):
        super().__init__()

        self.object = object

    def __rrshift__(self, process: _Process) -> _Process:
        stdin = typing.cast(typing.IO, process._process.stdin)
        assert stdin is not None

        if isinstance(stdin, io.TextIOWrapper):
            _v_ = self.object if isinstance(self.object, str) else self.object.decode()
            stdin.write(_v_)

        else:
            _v_ = self.object.encode() if isinstance(self.object, str) else self.object
            stdin.write(_v_)

        stdin.flush()
        return process

    def __add__(
        self, arguments: c_abc.Iterable
    ) -> "_PassStdout":  # `{process} >> write({string or bytes}) + {arguments}`
        return _PassStdout(self, arguments)

    def __sub__(
        self, arguments: c_abc.Iterable
    ) -> "_PassStderr":  # `{process} >> write({string or bytes}) - {arguments}`
        return _PassStderr(self, arguments)


write = _Write


class _PassStdout:
    def __init__(self, right_object, target_arguments):
        super().__init__()

        self.right_object = right_object
        self.target_arguments = target_arguments

        if isinstance(right_object, _Start):
            assert right_object.stdout in (None, subprocess.PIPE)
            right_object.pass_stdout = True

        elif isinstance(right_object, _Process):
            assert right_object.start.pass_stdout

        else:
            raise Exception

    def __rrshift__(self, left_object: typing.Union[c_abc.Iterable, _Process]) -> _Pass:
        # `{arguments} >> start() + {arguments}`
        # `{process} >> write() + {arguments}`
        return (left_object >> self.right_object) + self.target_arguments


class _PassStderr:
    def __init__(self, right_object, target_arguments):
        super().__init__()

        self.right_object = right_object
        self.target_arguments = target_arguments

        if isinstance(right_object, _Start):
            assert right_object.stderr in (None, subprocess.PIPE)
            right_object.pass_stderr = True

        elif isinstance(right_object, _Process):
            assert right_object.start.pass_stderr

        else:
            raise Exception

    def __rrshift__(self, left_object: typing.Union[c_abc.Iterable, _Process]) -> _Pass:
        # `{arguments} >> start() - {arguments}`
        # `{process} >> write() + {arguments}`
        return (left_object >> self.right_object) - self.target_arguments


class _Wait:
    def __init__(
        self,
        stdout: bool | typing.TextIO = True,
        stderr: bool | typing.TextIO = True,
        return_codes: c_abc.Container | None = (0,),
    ):
        super().__init__()

        self.stdout = stdout
        self.stderr = stderr
        self.return_codes = return_codes

    def __rrshift__(self, process: _Process) -> int:
        if process._source_process is not None:
            try:
                _v_ = _Wait(return_codes=process._source_process.start.return_codes)
                _ = process._source_process >> _v_

            except ProcessFailedError:
                raise ProcessFailedError(process)

        if process._process.stdin is not None:
            process._process.stdin.close()

        _v_ = process._stdout_queue is None or process.start.pass_stdout
        if not (_v_ or self.stdout is False):
            _v_ = sys.stdout if self.stdout is True else self.stdout
            self._print_stream("+|", process.get_stdout_strings(), _v_, process)

        _v_ = process._stderr_queue is None or process.start.pass_stderr
        if not (_v_ or self.stderr is False):
            _v_ = sys.stderr if self.stderr is True else self.stderr
            self._print_stream("-|", process.get_stderr_strings(), _v_, process)

        return_code = process._process.wait()

        if isinstance(process.start.stdout, (str, pathlib.Path)):
            typing.cast(typing.IO, process._stdout).close()

        if isinstance(process.start.stderr, (str, pathlib.Path)):
            typing.cast(typing.IO, process._stderr).close()

        if self.return_codes is not None and return_code not in self.return_codes:
            raise ProcessFailedError(process)

        return return_code

    def _print_stream(self, prefix, strings, file, process):
        strings = iter(strings)

        string = next(strings, None)
        if string is None:
            return

        print(process, file=file)
        print(prefix, string.replace("\n", f"\n{prefix}"), sep="", end="", file=file)
        for string in strings:
            print(string.replace("\n", f"\n{prefix}"), end="", file=file)

        print(file=file)
        file.flush()


class ProcessFailedError(Exception):
    def __init__(self, process: _Process):
        super().__init__(process)

        self.process = process

    def __str__(self):
        return self.process.get_chain_string()


wait = _Wait


class _Read:
    def __init__(
        self,
        stdout: bool | typing.TextIO = True,
        stderr: bool | typing.TextIO = False,
        bytes: bool = False,
        return_codes: c_abc.Container | None = (0,),
    ):
        super().__init__()

        self.stdout = stdout
        self.stderr = stderr
        self.bytes = bytes
        self.return_codes = return_codes

    def __rrshift__(
        self, process: _Process
    ) -> typing.AnyStr | tuple[typing.AnyStr, typing.AnyStr] | None:
        stdout = self.stdout is True
        stderr = self.stderr is True

        _ = process >> _Wait(
            stdout=(not self.stdout) if isinstance(self.stdout, bool) else self.stdout,
            stderr=(not self.stderr) if isinstance(self.stderr, bool) else self.stderr,
            return_codes=self.return_codes,
        )

        stdout_object = (
            (
                b"".join(process.get_stdout_bytes())
                if self.bytes
                else "".join(process.get_stdout_strings())
            )
            if stdout
            else None
        )
        stderr_object = (
            (
                b"".join(process.get_stderr_bytes())
                if self.bytes
                else "".join(process.get_stderr_strings())
            )
            if stderr
            else None
        )

        if stdout and stderr:
            _v_ = tuple[typing.AnyStr, typing.AnyStr]
            return typing.cast(_v_, (stdout_object, stderr_object))

        if stdout:
            return typing.cast(typing.AnyStr, stdout_object)

        if stderr:
            return typing.cast(typing.AnyStr, stderr_object)


read = _Read
