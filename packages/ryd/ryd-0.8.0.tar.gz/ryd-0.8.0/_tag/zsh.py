# coding: 'utf-8'

from __future__ import annotations

from ryd._tag._handler import ProgramHandler
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ryd._convertor._base import ConvertorBase
else:
    ConvertorBase = Any


class Zsh(ProgramHandler):
    def __init__(self, convertor: ConvertorBase) -> None:
        super().__init__(convertor)
        self._pre = ''

    def pre(self, d: Any) -> None:
        self._pre = str(d)

    def __call__(self, d: Any) -> None:
        """
        run each line in zsh, interspacing the lines with the output
        """
        s = self.run_line_by_line('zsh', d, pre=self._pre, extra=True)
        self.c.add_code(s, 'console')

    def hidden(self, d: Any) -> None:
        self.run_line_by_line('zsh', d, pre=self._pre, extra=True)
