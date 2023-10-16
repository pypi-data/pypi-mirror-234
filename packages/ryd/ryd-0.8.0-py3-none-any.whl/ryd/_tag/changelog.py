from __future__ import annotations

import datetime
from ryd._tag._handler import BaseHandler
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ryd._convertor._base import ConvertorBase
else:
    ConvertorBase = Any


class Changelog(BaseHandler):
    def __init__(self, convertor: ConvertorBase) -> None:
        super().__init__(convertor)

    def __call__(self, d: Any) -> None:
        """
        input is a mapping keys are (version, date) tuples, or the word NEXT
        value must be a list of individual changes
        """
        assert isinstance(d, dict)
        for key, value in d.items():
            if isinstance(key, str):
                assert key == 'NEXT'
            else:
                assert len(key) == 2
                assert isinstance(key[1], datetime.date)
        self.c.add_changelog(d)
