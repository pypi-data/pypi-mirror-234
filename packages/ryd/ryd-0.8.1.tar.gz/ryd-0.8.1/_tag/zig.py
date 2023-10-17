# coding: 'utf-8'

from __future__ import annotations

import os
import subprocess
from typing import Any, TYPE_CHECKING
from ryd._tag._handler import ProgramHandler

if TYPE_CHECKING:
    from ryd._convertor._base import ConvertorBase
else:
    ConvertorBase = Any


class Zig(ProgramHandler):
    def __init__(self, convertor: ConvertorBase) -> None:
        super().__init__(convertor)
        self._pre = ''

    def pre(self, d: Any) -> None:
        """Prefix all following ``!zig`` documents with this document (e.g. used for ``@import``s)

        This part will not be be shown. The content should be a zig snippet, that
        will be used as prefix for following programs which can be incomplete.
        This is useful for suppressing repetetive import statements.
        """
        self._pre = str(d)

    def __call__(self, d: Any) -> None:
        """
        Include Zig program in text. Prefix and execute setting !stdout.
        """
        s = str(d)
        sd = self._pre + s
        old_dir = os.getcwd()
        self.c.temp_dir.chdir()  # type: ignore
        self.c.last_compile = self.c.check_output(sd, ['zig', 'build-exe', None], '.zig')
        os.chdir(old_dir)
        assert self.c.last_source is not None
        exe = self.c.last_source.with_suffix("")
        if exe.exists():
            self.c.last_output = subprocess.check_output([exe], encoding='utf-8')
        else:
            print(f'executable {exe} not found')
        self.c.add_code(s, 'zig')

    def hidden(self, d: Any) -> None:
        s = str(d)
        sd = self._pre + s
        self.c.check_output(sd)

    def roundtrip(self, s: bytes) -> bytes | None:
        print('zig roundtrip', s)
        try:
            cmd = ['zig', 'fmt', '--stdin']
            p = subprocess.Popen(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE
            )
            res = p.communicate(input=s)
        except Exception as e:
            print('error', e)
            if hasattr(e, 'output'):
                print(e.output.decode('utf-8'))
            return None
        return res[0]
