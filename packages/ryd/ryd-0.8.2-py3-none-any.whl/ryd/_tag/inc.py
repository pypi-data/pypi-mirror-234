# coding: 'utf-8'

from __future__ import annotations

from pathlib import Path
from typing import Any, Union, TYPE_CHECKING

from ryd._tag._handler import BaseHandler

if TYPE_CHECKING:
    from ryd._convertor._base import ConvertorBase
else:
    ConvertorBase = Any


class Inc(BaseHandler):
    def __init__(self, convertor: ConvertorBase) -> None:
        super().__init__(convertor)
        self.is_code = True

    def __call__(self, d: Any, typ: Union[str, None] = None) -> None:
        """Include the content of the listed files (indented), without other processing, \
         into the output. Preceed with ``::`` if necessary

        If a file name doesn't start with ``/``, it is considered to be relative to the
        directory of the output path.
        """
        for s in self._process_files(d):
            self.c.add_code(s)

    def raw(self, d: Any) -> None:
        """Include the listed files raw (i.e. without processing, or indenting) into the output.

        If a file name doesn't start with ``/``, it is considered to be relative to the
        directory of the output path.
        """
        for s in self._process_files(d):
            self.c.add_text(s)

    def _process_files(self, d: Any) -> Any:
        base_dir = None
        if isinstance(d, list):
            lines = d
        else:
            lines = str(d).strip().splitlines()
        for line in lines:
            if not line:
                continue
            if '{tempdir}' in line and line[0] != '/':
                # is tempdir an instance?
                raise NotImplementedError
                # p = Path(line.format(tempdir=self.tempdir.directory))
            elif base_dir is not None and line[0] != '/':
                p = base_dir / line
            elif base_dir is not None and line[0] == '~':
                p = Path(line).expanduser()
            else:
                p = Path(line)
            yield p.read_text()
