"""
minimal wrapper around sys.stdout so you can do:
    some_var = Path(self._args.path) if self._args.path else stdout
    with self.open('w') as fp:
        print(...., file=fp)
"""

import sys
from typing import Optional, Any, Type, Literal, TextIO
from types import TracebackType

from ruamel.std.pathlib import Path


class SysStdOut:
    def __init__(self) -> None:
        self.parent = Path('')

    def __enter__(self) -> TextIO:
        return sys.stdout

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Literal[False]:
        return False

    def open(self, *args: Any, **kw: Any) -> Any:
        return self

    def exists(self) -> Literal[False]:
        return False

    def unlink(self) -> None:
        pass


sys_stdout = SysStdOut()
