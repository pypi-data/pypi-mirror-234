# coding: 'utf-8'

from __future__ import annotations

from ryd._tag._handler import BaseHandler
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ryd._convertor._base import ConvertorBase
else:
    ConvertorBase = Any


class Code(BaseHandler):
    def __init__(self, convertor: ConvertorBase) -> None:
        super().__init__(convertor)

    def __call__(self, d: Any) -> None:
        """
        Include program in text. Do not mark as executable, doesn't influence ``!stdout``.
        """
        s = str(d)
        self.c.add_code(s)
