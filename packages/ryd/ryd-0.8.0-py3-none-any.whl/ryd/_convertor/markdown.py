# coding: utf-8

from __future__ import annotations

"""

There are no special characters to introduce indented code blocks (i.e like .rst
has ::), unless you want to provide info then use e.g ```python. Otherwise code is
indented by four spaces.

"""

import sys
from ruamel.yaml.comments import TaggedScalar, CommentedSeq, CommentedMap
from ruamel.yaml.scalarstring import LiteralScalarString
from ruamel.std.pathlib import Path
from ruamel.yaml import YAML

from typing import Optional, Dict, Any, List, Union, TextIO

from ryd.ryd import RYD, RydExecError
from ryd.classes_0_1 import (
    IncRaw,
    Inc,
    Nim,
    NimPre,
    Python,
    PythonPre,
    Code,
    Stdout,
    StdoutRaw,
    Comment,
)
from ryd.sys_stdout import sys_stdout, SysStdOut
from ._base import Convertor_0_1, Convertor_0_2


class MdText:
    def __init__(self, s: str) -> None:
        self.s = s

    def dump(self, fp: TextIO) -> None:
        fp.write(self.s)
        if self.s and self.s[-1] != '\n':
            fp.write('\n')


class MdCode:
    def __init__(self, s: str, typ: Optional[str] = None) -> None:
        self.s = s
        self.typ = typ

    def dump(self, fp: TextIO) -> None:
        t = self.typ if self.typ else 'lang-none'
        fp.write(f'\n```{t}\n')
        fp.write('\n'.join(self.s.strip().splitlines()))
        fp.write('\n```\n')


class MdTable:
    def __init__(self, s: Any) -> None:
        """input is a list of lists, generate multicolumn headerless table"""
        self.s = s

    def dump(self, fp: TextIO) -> None:
        fp.write('<table class="docutils">\n')
        for row in self.s:
            fp.write('  <tr>')
            for elem in row:
                elem = str(elem)
                if elem.startswith('https:') or elem.startswith('http:'):
                    elem = f'<a href="{elem}">{elem}</a>'
                fp.write(f'    <td>{elem}</td>\n')
            fp.write('  </tr>\n')
        fp.write('</table>\n')


class MdChangelog:
    def __init__(self, s: Any) -> None:
        """input is a dict, generate changelog entries"""
        self.s = s

    def dump(self, fp: TextIO) -> None:
        for key, entries in self.s.items():
            if isinstance(key, str):
                fp.write(f'{key}:<br>\n')
            else:
                fp.write(f'\n{key[0]} ({key[1]}):\n\n')
            for entry in entries:
                fp.write(f'- {entry}\n')


class MarkdownConvertor2(Convertor_0_2):
    def __init__(self, ryd: RYD, yaml: YAML, md: Dict[str, Any], path: Path) -> None:
        super().__init__(ryd, yaml, md, path)
        self.output: List[Any] = []
        if getattr(self._ryd._args, 'stdout', False):
            self._out_name = None
            self._out_path = SysStdOut
        else:
            self._out_path = self._path.with_suffix('.md')  # type: ignore
            self._out_name = self._out_path
        self.last_code = False
        self.ofp: Union[TextIO, None] = None
        self.start_line = [0]

    def add_text(self, s: str) -> None:
        self.output.append(MdText(s))

    def add_code(self, s: str, typ: Optional[str] = None) -> None:
        self.output.append(MdCode(s, typ))

    def add_last_output(self, typ: Optional[str] = None, raw: bool = False) -> None:
        if self.last_output:
            if raw:
                self.add_text(self.last_output)
            else:
                self.add_code(self.last_output, typ=typ)

    def add_last_compiler_output(self, typ: Optional[str] = None) -> None:
        if self.last_compile:
            self.add_code(self.last_compile, typ=typ)

    def add_table(self, s: Any) -> None:
        self.output.append(MdTable(s))

    def add_changelog(self, s: Any) -> None:
        self.output.append(MdChangelog(s))

    def write(self) -> Union[None, Path]:
        """this builds up a list of output sections, processing the input
        The output doesn't have to match the input as input can cause no output or more
        than one output"""

        out_ok = True
        # might need to know the basedir of the output
        for d in self.input:
            if isinstance(d, TaggedScalar):
                try:
                    tag, fun = self.get_tag(d)
                    typ = self.get_instance(tag)
                    if fun is not None:
                        try:
                            getattr(typ, fun)(d.value)
                        except AttributeError:
                            # res = getattr(typ, '_unknown')(fun, d.value)
                            typ._unknown(fun, d.value)
                    else:
                        typ(d.value)
                except RydExecError:
                    out_ok = False
            elif isinstance(d, LiteralScalarString):
                s = str(d)
                self._line = self._yaml.reader.line - s.count('\n') + 1
                self.add_text(s)
            elif isinstance(d, (CommentedSeq, CommentedMap)):
                try:
                    tag, fun = self.get_tag(d)
                    typ = self.get_instance(tag)
                    if fun is not None:
                        try:
                            getattr(typ, fun)(d)
                        except AttributeError:
                            typ._unknown(fun, d)
                    else:
                        typ(d)
                except RydExecError:
                    out_ok = False
            else:
                print('<<<<<<<<<<<<<<<<<< d', type(d), d)
            if not out_ok:
                print('>>> there was an execution error <<<')
            sys.stdout.flush()
        # print('dumping', len(self.input), len(self.output))
        with self._out_path.open('w') as ofp:  # type: ignore
            for d in self.output:
                d.dump(ofp)
        return self._out_name  # type: ignore


class MarkdownConvertor(Convertor_0_1):
    def __init__(self, ryd: RYD, yaml: YAML, md: Dict[str, Any], path: Path) -> None:
        super().__init__(ryd)
        self._yaml = yaml
        for v in self._tag_obj.values():
            yaml.register_class(v)
        self._md = md
        self._path = path
        if self._ryd._args.stdout:
            self._out_path = sys_stdout
        else:
            self._out_path = self._path.with_suffix('.md')
        self.updated = True
        ####
        self.data: List[Any] = []
        self.nim_pre = ""
        self.python_pre = ""
        self.last_output: Union[str, None] = ""

    def __call__(self, s: Any) -> bool:
        """
        s is the data from a single load from load_all
        returns True if correctly parsed
        """
        self.data.append(s)
        return True

    def write(self) -> None:
        with self._out_path.open('w') as fp:
            self.dump(fp, base_dir=self._out_path.parent)

    def dump(self, fp: TextIO = sys.stdout, base_dir: Optional[Path] = None) -> None:
        last_ended_in_double_newline = False
        last_code = False
        for d in self.data:
            # print(type(d))
            if isinstance(d, IncRaw):
                if last_code:
                    last_code = False
                    fp.write('\n')
                for line in d.strip().splitlines():
                    if not line:
                        continue
                    if base_dir is not None and line[0] != '/':
                        p = base_dir / line
                    else:
                        p = Path(line)
                    print(p.read_text(), file=fp, end="")
            elif isinstance(d, Inc):
                if last_code:
                    last_code = False
                    print('', file=fp)
                for line in d.strip().splitlines():
                    if not line:
                        continue
                    if base_dir is not None and line[0] != '/':
                        p = base_dir / line
                    else:
                        p = Path(line)
                    for line in p.open():
                        if line.strip():
                            print('    ', line, sep="", end="", file=fp)
                        else:
                            print("", line, sep="", end="", file=fp)
            elif isinstance(d, (Nim, Python, Code)):
                if d:
                    if not last_ended_in_double_newline:
                        print('\n', file=fp)
                    for line in d.strip().splitlines():
                        if line.strip():
                            print('    ', line, sep="", file=fp)
                        else:
                            print('', line, sep="", file=fp)
                    last_code = True
                if isinstance(d, Nim):
                    self.last_output = self.check_nim_output(self.nim_pre + d)  # type: ignore
                    if self._ryd._args.verbose > 1:
                        print('=========== output =========')
                        print(self.last_output, end="")
                        print('============================')
                    if self.last_output is None:
                        sys.exit(1)
                if isinstance(d, Python):
                    self.last_output = self.check_output(self.python_pre + d)
                    if self._ryd._args.verbose > 1:
                        print('=========== output =========')
                        print(self.last_output, end="")
                        print('============================')
                    if self.last_output is None:
                        sys.exit(1)
            elif isinstance(d, NimPre):
                self.nim_pre = d
            elif isinstance(d, PythonPre):
                self.python_pre = d
            elif isinstance(d, Comment):
                pass
            else:
                assert isinstance(self.last_output, str)
                drs = d.rstrip()
                last_ended_in_double_newline = True
                d = type(d)(drs + '\n\n')
                if last_code:
                    last_code = False
                    fp.write('\n')
                print(d, file=fp, end="")
                if isinstance(d, (Stdout, StdoutRaw)):
                    prefix = "" if isinstance(d, StdoutRaw) else '    '
                    for line in self.last_output.rstrip().splitlines():
                        print('{}{}'.format(prefix, line), file=fp)
                    last_code = True
                elif type(d) != LiteralScalarString:
                    print('found unknown document type:', type(d))
                    try:
                        print('tag', d.tag)
                    except AttributeError:
                        pass
                    sys.exit(1)
                # print(file=fp)
