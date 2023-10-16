# coding: 'utf-8'

from __future__ import annotations

from ryd._tag._handler import BaseHandler
from typing import Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ryd._convertor._base import ConvertorBase
else:
    ConvertorBase = Any


class Comment(BaseHandler):
    def __init__(self, convertor: ConvertorBase) -> None:
        super().__init__(convertor)

    def __call__(self, d: Any, typ: Union[str, None] = None) -> None:
        """The whole document will be discarded, i.e. not included in the output.

        This allows commenting out complete sections in an output independent way.
        """
        return

    def _unknown(self, typ: str, value: str) -> None:
        """ you can put comment- for any tag to comment it out """
        pass
