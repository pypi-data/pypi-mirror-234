from __future__ import annotations

import datetime
import ruamel.yaml
from pathlib import Path
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
        if isinstance(d, str):
            # load first two minor version number changes from the specified file name
            # that file should have keys (except for temporary NEXT) that consist of
            # version number/date tuples
            # if you specify a directory, ryd will chdir into that
            path = Path(d)
            if not path.exists():
                path = Path('..') / d
            assert path.exists()
            yaml = ruamel.yaml.YAML(typ='safe', pure=True)
            x = yaml.load(path)
            d = {}
            mins = None
            changes = 2
            for k2, v2 in x.items():
                if isinstance(k2, tuple):
                    # assume some dotted number
                    major, minor = [int(x) for x in k2[0].split('.', 2)[:2]]
                    if mins is None:
                        mins = [major, minor]
                    else:
                        if mins != [major, minor]:
                            changes -= 1
                            mins = [major, minor]
                if changes <= 0:
                    break
                d[k2] = v2
        assert isinstance(d, dict)
        for key, value in d.items():
            if isinstance(key, str):
                assert key == 'NEXT'
            else:
                assert len(key) == 2
                assert isinstance(key[1], datetime.date)
        self.c.add_changelog(d)
