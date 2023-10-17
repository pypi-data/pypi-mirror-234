# coding: 'utf-8'

from __future__ import annotations

# import sys
# import time
import subprocess
from typing import Any, TYPE_CHECKING, Optional, Union
from pathlib import Path

if TYPE_CHECKING:
    from ryd._convertor._base import ConvertorBase
else:
    ConvertorBase = Any


class BaseHandler:
    def __init__(self, convertor: ConvertorBase) -> None:
        self._convertor = convertor
        self.is_code = False

    @property
    def c(self) -> ConvertorBase:
        return self._convertor

    def _unknown(self, fun_name: str, value: str) -> None:
        print(f'>>> Unknown method "{fun_name}", on {self.__class__.__name__} <<<')


class ProgramHandler(BaseHandler):
    def __init__(self, convertor: ConvertorBase) -> None:
        super().__init__(convertor)
        self.is_code = True

    def run(self, cmd: str) -> Any:
        return None

    # def run_line_by_line2(self, d: Any) -> str:
    #     """doesn't work for more than one line of input"""
    #     ret_val = []
    #     cmd = ['zsh']
    #     p = subprocess.Popen(
    #         *cmd,
    #         stdin=subprocess.PIPE,
    #         stdout=subprocess.PIPE,
    #         pipesize=1,
    #         bufsize=0,
    #         encoding='utf-8',
    #     )
    #     retcode = p.poll()
    #     prompt = '% '
    #     lines = str(d).splitlines()
    #     for idx, line in enumerate(lines):
    #         line_out = ''
    #         ret_val.append(prompt + line)
    #         p.stdin.write(line + '\n')
    #         print('sending', line)
    #         if idx == len(lines) - 1:
    #             print('closing process stdin')
    #             p.stdin.close()
    #         else:
    #             print('flusing process stdin')
    #             p.stdin.flush()
    #         while retcode is None:
    #             line_out = p.stdout.readline()
    #             if not line_out:
    #                 break
    #             # data = p.stdout.read(1)
    #             # if data:
    #             #     if data == '\n':
    #             #         ret_val.append(line_out)
    #             #         line_out = ''
    #             #     else:
    #             #         line_out += data
    #             # else:
    #             #     time.sleep(0.2)  # only sleep if there is nothing to read
    #             retcode = p.poll()
    #     data = p.stdout.read()
    #     if data or line_out:
    #         lines = line_out + data
    #         for line in lines.split():
    #             ret_val.append(line)
    #     return '\n'.join(ret_val) + '\n'

    def run_line_by_line(
        self, cmd: Union[str, Path], d: Any, pre: Optional[Any] = None, extra: bool = False
    ) -> str:
        """"""
        ret_val = []
        p = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8'
        )
        # retcode = p.poll()
        prompt = '% '
        divider = '+=++=+'
        lines = str(d).splitlines()
        split_pre = str(pre).splitlines() if pre else []
        in_lines = []
        for line in split_pre + lines:
            in_lines.append(line)
            in_lines.append(f'echo "{divider}"')
        res = p.communicate('\n'.join(in_lines[:-1]) + '\n')  # don't use last divider
        split_res = res[0].split(divider + '\n')
        if len(split_res) != len(lines) + len(split_pre):
            print('inlines', in_lines)
            print('split_res', split_res)
            print('res', res)
            print(len(split_res), len(lines), len(split_pre))
        for idx, line in enumerate(lines):
            ret_val.append(prompt + line)
            out = split_res[idx + len(split_pre)].rstrip()
            if out:
                ret_val.append(out)
        if extra:
            ret_val.append(prompt)
        return '\n'.join(ret_val) + '\n'
