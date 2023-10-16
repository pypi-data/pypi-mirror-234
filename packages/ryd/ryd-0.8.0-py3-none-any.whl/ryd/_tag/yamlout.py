# coding: 'utf-8'

from __future__ import annotations

from ryd._tag.stdout import Stdout
from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ryd._convertor._base import ConvertorBase
else:
    ConvertorBase = Any


class Yamlout(Stdout):
    def __init__(self, convertor: ConvertorBase) -> None:
        super().__init__(convertor)

    def __call__(self, d: Any, typ: Optional[str] = None) -> None:
        """
        Include output from last executable document (e.g. ``!python``) as code tagged as \
        YAML document.
        """
        return super().__call__(d, 'yaml')
