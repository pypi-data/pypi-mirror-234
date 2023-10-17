# coding: 'utf-8'

from __future__ import annotations

import subprocess
from typing import Any, TYPE_CHECKING
from ryd._tag._handler import ProgramHandler

if TYPE_CHECKING:
    from ryd._convertor._base import ConvertorBase
else:
    ConvertorBase = Any


class Nim(ProgramHandler):
    def __init__(self, convertor: ConvertorBase) -> None:
        super().__init__(convertor)
        self._pre = ''

    def pre(self, d: Any) -> None:
        """Prefix all following ``!nim`` documents with this document (e.g. used for imports)

        This part will not be be shown. The content should be a nim snippet, that
        will be used as prefix for following programs which can be incomplete.
        This is useful for  suppressing repetetive import statements.
        """
        self._pre = str(d)

    def __call__(self, d: Any) -> None:
        """Include Nim program in text. Prefix and mark as executable.
        """
        s = str(d)
        sd = self._pre + s
        self.c.last_compile = self.c.check_output(
            sd, ['nim', 'compile', '--verbosity:0', '--hint[Processing]:off', None], '.nim'
        )
        assert self.c.last_source is not None
        exe = self.c.last_source.with_suffix("")
        if exe.exists():
            self.c.last_output = subprocess.check_output([exe], encoding='utf-8')
        else:
            print(f'executable {exe} not found')
        self.c.add_code(s, 'nim')

    # def hidden(self, d: Any) -> None:
    #     s = str(d)
    #     sd = self._pre + s
    #     self.c.check_output(sd)

# class UnPy(RydProgram):
#     """Include Nim program in text. Do not mark as executable. Set output to result of unpy.
#     """
#
#     yaml_tag = '!unpy'
#
#     def check_output(self, convertor: ConvertorBase) -> Union[str, None]:
#         # None is replaced by the filename
#         return convertor.check_output(
#             self, exe=['unpy', 'update', '--output:-', None], ext='.nim'
#         )
