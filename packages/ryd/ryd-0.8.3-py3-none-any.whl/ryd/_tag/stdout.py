# coding: 'utf-8'

from __future__ import annotations

from ryd._tag._handler import BaseHandler
from typing import Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ryd._convertor._base import ConvertorBase
else:
    ConvertorBase = Any


class Stdout(BaseHandler):
    def __init__(self, convertor: ConvertorBase) -> None:
        super().__init__(convertor)
        self.is_code = True

    def __call__(self, d: Any, typ: Union[str, None] = None) -> None:
        """
        Include output from last executable document (e.g. ``!python``) as code.
        """
        s = str(d)
        self.c.add_text(s)
        self.c.add_last_output(typ=typ)

    def raw(self, d: Any, typ: Union[str, None] = None) -> None:
        """
        Include output from the last program, as source text for the output format.

        This can be used to e.g. have a program generate an definition list programmatically.
        """
        s = str(d)
        self.c.add_text(s)
        self.c.add_last_output(typ=typ, raw=True)
