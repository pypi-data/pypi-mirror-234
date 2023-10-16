# coding: 'utf-8'

from __future__ import annotations

import sys
import subprocess
import datetime
from typing import Optional, Any, Union, Dict, List, TextIO
from ruamel.yaml import YAML
from ruamel.yaml.comments import TaggedScalar, CommentedSeq, CommentedMap
from ruamel.yaml.scalarstring import LiteralScalarString
from ruamel.std.pathlib import Path
from ryd.ryd import RYD, RydExecError
from ryd.classes_0_1 import (
    IncRaw,
    Inc,
    Python,
    PythonPre,
    Code,
    Stdout,
    StdoutRaw,
    Comment,
    PythonHidden,
    LastCompile,
)
from ryd.sys_stdout import SysStdOut
from ._base import Convertor_0_1, Convertor_0_2

# the _0_1 convertors all interpret what to do with the
# individual tagged literal scalars, and information like e.g. if
# a preceding document ended in a double colon is known by the convertor
# and not asked by the RyDoc type of its predecessor
#
# in 0_2 the convertor
# [v] no pre-registering
# [v] automatic split of lang-xyz in language (lang) and specification (xyz)
#     creating an instance of class Lang with specification xyz (which can
#     come from the parent class of Lang (and thus implement python-hidden, python-pre
#     python-post, etc in a reusable way).
# [?] attachment of information is to a dict attribute on the convertor,
#     this can be get() taking into account a non-existing value (output
#     of a program, compile result of a program)
# [?] handle '--- !./example.py |' as writing out that file, using
#     auto-execution flag in the config document
# [v] add !yamlout processing ( to get pygments .. code:: yaml )
#     peg, shell etc exist as well
# [?] should have a class attribute for tag, file extension
# [ ] run a command (e.g. oitnb) on all content with a tag matching pattern
# [ ] allow to diff with different version, syncing on documents, and detecting
#     documents inserted in the middle (e.g. extra program).


class RstText:
    def __init__(self, s: str) -> None:
        self.s = s

    def dump(self, fp: TextIO) -> None:
        fp.write(self.s)
        if self.s and self.s[-1] != '\n':
            fp.write('\n')


class RstCode:
    def __init__(self, s: str, typ: Optional[str] = None) -> None:
        self.s = s
        self.typ = typ

    def dump(self, fp: TextIO) -> None:
        """RST code blocks are indented, but don't add indentation to empty lines"""
        t = ' ' + self.typ if self.typ else ''
        fp.write(f'\n.. code::{t}\n')
        fp.write(''.join(('\n  ' if z else '\n') + z for z in self.s.splitlines()))
        fp.write('\n\n')


class RestructuredTextConvertor2(Convertor_0_2):
    def __init__(self, ryd: RYD, yaml: YAML, md: Dict[str, Any], path: Path) -> None:
        super().__init__(ryd, yaml, md, path)
        # outpath has to be set in the init
        self._out_path = self._path.with_suffix('.rst')
        self.output: List[Any] = []
        self.last_code = False
        self.ofp: Union[TextIO, None] = None

    def roundtrip(self, d: Any, src: bytes) -> bool:
        m = None
        if isinstance(d, TaggedScalar):
            tag, fun = self.get_tag(d)
            typ = self.get_instance(tag)
            if fun is not None:
                try:
                    m = getattr(typ, 'roundtrip_' + fun, None)
                except AttributeError:
                    pass
            if m is None:
                m = getattr(typ, 'roundtrip', None)
        if m is not None:
            tl, rest = src.split(b'\n', 1)
            res = m(rest)
            if res is not None:
                self.output.append(tl + b'\n' + res)
                return True
        self.output.append(src)
        return True

    def roundtrip_write(self, p: Path, yaml: YAML, cx: Any) -> None:
        print('roundtrip writing', p)
        with p.open('wb') as fp:
            yaml.dump(cx, fp)
            for x in self.output:
                fp.write(x)
        # print((b''.join(self.output)).decode('utf-8'), self._out)

    def check(self) -> bool:
        if (
            not self._ryd._args.force
            and self._out_path.exists()
            and self._path.stat().st_mtime < self._out_path.stat().st_mtime
        ):
            if self._ryd._args.verbose > 0:
                print('skipping', end=' ')
                self._ryd.name()
            return False
        return True

    def rst2pdf(self, file_path: Path) -> Path:
        if self._ryd._args.verbose > 0:
            print('generating PDF')
        fn = str(file_path)
        res = subprocess.check_output(  # NOQA
            ['rst2pdf', fn, '-s', 'freetype-sans,eightpoint'], encoding='utf-8'
        )
        return file_path.with_suffix('.pdf')

    def rst2html(self, file_path: Path) -> Path:
        if self._ryd._args.verbose > 0:
            print('generating HTML')
        fn = str(file_path)
        res = subprocess.check_output(['rst2html', fn], encoding='utf-8')  # NOQA
        html_path = file_path.with_suffix('.html')
        html_path.write_text(res)
        return html_path

    def embedhtml(self, file_path: Path) -> None:
        if self._ryd._args.verbose > 0:
            print('embedding HTML')
        fn = str(file_path)
        res = subprocess.check_output(['webpage2html', '-o', fn, fn], encoding='utf-8')
        if res:
            print('embed:', res)

    def add_text(self, s: str) -> None:
        self.output.append(RstText(s))

    def add_code(self, s: str, typ: Optional[str] = None) -> None:
        self.output.append(RstCode(s, typ))

    def add_last_output(self, typ: Optional[str] = None, raw: bool = False) -> None:
        if self.last_output:
            if raw:
                self.add_text(self.last_output)
            else:
                self.add_code(self.last_output, typ=typ)

    def add_last_compiler_output(self, typ: Optional[str] = None) -> None:
        if self.last_compile:
            self.add_code(self.last_compile, typ=typ)

    def write(self) -> None:
        """this builds up a list of output sections, processing the input
        The output doesn't have to match the input as input can cause no output or more
        than one output"""

        rst_ok = True
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
                    # if res is not None:
                    #     self.raw_out(res)
                    # # print('tag', tag, fun, d.value)
                    # if typ.is_code:
                    #     self.last_code = True
                except RydExecError:
                    rst_ok = False
            elif isinstance(d, LiteralScalarString):
                s = str(d)
                if self.metadata.get('tasklist'):
                    s = self.tasklistify(s)
                self._line = self._yaml.reader.line - s.count('\n') + 1
                self.check_backquotes(s)
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
                    rst_ok = False
            else:
                print('<<<<<<<<<<<<<<<<<< d', type(d), d.value)
            if not rst_ok:
                print('>>> there was an execution error <<<')
            sys.stdout.flush()
        # print('dumping', len(self.input), len(self.output))
        with self._out_path.open('w') as ofp:
            for d in self.output:
                d.dump(ofp)
        # pdf/html as the commandline options are try-state if specifying --no-pdf
        # or --no-html, don't generate output even if set in the metadata
        if self._ryd._args.pdf is not False:
            if (
                self._ryd._args.pdf
                or self.metadata.get('post') == 'pdf'
                or self.metadata.get('pdf')
            ):
                pdf_path = self.rst2pdf(self._out_path)
                if self.metadata.get('encrypt'):
                    pw = self.metadata['encrypt']['passwd']
                    # print('pw', pw, file=sys.stderr)
                    assert isinstance(self._out_path, Path)
                    enc_file = pdf_path.with_suffix(
                        '.{:%Y%m%d}.pdf'.format(datetime.date.today())
                    )
                    # self._out_path.rename(tmp_file)
                    subprocess.check_output(
                        ['pdftk', str(pdf_path), 'output', str(enc_file), 'user_pw', pw]
                    )
        if self._ryd._args.html is not False:
            if self._ryd._args.html or self.metadata.get('post') == 'html':
                html_path = self.rst2html(self._out_path)
                if self._ryd._args.embed or self.metadata.get('embed'):
                    self.embedhtml(html_path)

    task_map = {  # newlines as I don't know how to replace normal list bullet
        '[ ]': '\n☐',
        '[v]': '\n☑',
        '[x]': '\n☒',
    }

    def tasklistify(self, s: str) -> str:
        res = []
        for line in s.splitlines(True):
            lsline = line.lstrip()
            for k, v in self.task_map.items():
                if lsline.startswith(k):
                    line = line.replace(k, v, 1)
                    break
            res.append(line)
        return ''.join(res)

    def check_backquotes(self, s: Any) -> bool:
        """check for single backquotes"""
        # if isinstance(s, RydDoc) and not isinstance(s, Python):
        #     print(type(s))
        if isinstance(s, Python):
            return False
        # find all backquotes in document
        bqs = []
        # character index in file to beginning of each line
        lines: List[Union[int, None]] = [0]
        line = 0
        col = 0
        for idx, ch in enumerate(s):
            if ch == '`':
                bqs.append((idx, line, col))
            elif ch == '\n':
                lines.append(idx + 1)
                line += 1
                col = 0
                continue
            col += 1
        lines.append(None)  # for last line
        bqidx = 0
        last_line_displayed = -1
        while bqidx < len(bqs):
            lnr = bqs[bqidx][1]
            # ``pair of double backquotes`` -> code
            try:
                assert isinstance(lines[lnr], int)
                tlnr: int = lines[lnr]  # type: ignore
                if s[tlnr] == ' ' and s[tlnr + 1] == ' ':
                    # first characters on line are spaces -> code/ryd example
                    bqidx += 1
                    continue
            except IndexError:
                print('error')
                pass
            if (
                bqidx + 3 <= len(bqs)
                and bqs[bqidx][0] + 1 == bqs[bqidx + 1][0]
                and bqs[bqidx + 2][0] + 1 == bqs[bqidx + 3][0]
            ):
                bqidx += 4
                continue
            # unmatched double backquotes
            # if bqidx + 1 <= len(bqs) and \
            #    bqs[bqidx][0] + 1 ==  bqs[bqidx+1][0]:

            # :cmd:`some string`
            if bqidx > 0 and s[bqs[bqidx][0] - 1] == ':':
                bqidx += 2
                continue
            # `some <url>`_
            try:
                if bqidx + 1 < len(bqs) and s[bqs[bqidx + 1][0] + 1] == '_':
                    bqidx += 2
                    continue
            except IndexError:
                pass  # probably end of file
            self._ryd.name()
            if lnr != last_line_displayed:
                print(
                    '{}: {}'.format(lnr + self._line, s[lines[lnr] : lines[lnr + 1]]), end=""
                )

                last_line_displayed = lnr
            print(' ' * (-1 + len(str(lnr + self._line)) + bqs[bqidx][2]), '--^')
            bqidx += 1
        return False


class RestructuredTextConvertor(Convertor_0_1):
    def __init__(self, ryd: RYD, yaml: YAML, md: Dict[str, Any], path: Path) -> None:
        super().__init__(ryd)
        self._yaml = yaml
        for v in self._tag_obj.values():
            yaml.register_class(v)
        self._md = md
        self._path = path
        # outpath has to be set in the init
        self._out_path = self._path.with_suffix('.rst')
        self.data: List[Any] = []
        ####
        self.last_output: Union[str, None] = ""
        self.updated = False
        self.python_pre = ""
        # register all defined classes and store tag + comment

    def check(self) -> bool:
        if (
            not self._ryd._args.force
            and self._out_path.exists()
            and self._path.stat().st_mtime < self._out_path.stat().st_mtime  # type: ignore
        ):
            if self._ryd._args.verbose > 0:
                print('skipping', end=' ')
                self._ryd.name()
            return False
        return True

    def __call__(self, s: Any) -> bool:
        try:
            # this is no longer valid if splitting
            self._line = self._yaml.reader.line - s.count('\n') + 1
        except AttributeError:
            print('error getting s.count', s)
            raise
        sx = self.update(s)
        if sx:
            raise NotImplementedError
            self.updated = True
            self.data.append(sx)
        else:
            self.data.append(s)
        return True

    def update(self, s: Any) -> bool:
        # if isinstance(s, RydDoc) and not isinstance(s, Python):
        #     print(type(s))
        if isinstance(s, Python):
            return False
        # find all backquotes in document
        bqs = []
        # character index in file to beginning of each line
        lines: List[Union[int, None]] = [0]
        line = 0
        col = 0
        for idx, ch in enumerate(s):
            if ch == '`':
                bqs.append((idx, line, col))
            elif ch == '\n':
                lines.append(idx + 1)
                line += 1
                col = 0
                continue
            col += 1
        lines.append(None)  # for last line
        bqidx = 0
        last_line_displayed = -1
        while bqidx < len(bqs):
            lnr = bqs[bqidx][1]
            # ``pair of double backquotes`` -> code
            try:
                assert isinstance(lines[lnr], int)
                tlnr: int = lines[lnr]  # type: ignore
                if s[tlnr] == ' ' and s[tlnr + 1] == ' ':
                    # first characters on line are spaces -> code/ryd example
                    bqidx += 1
                    continue
            except IndexError:
                print('error')
                pass
            if (
                bqidx + 3 <= len(bqs)
                and bqs[bqidx][0] + 1 == bqs[bqidx + 1][0]
                and bqs[bqidx + 2][0] + 1 == bqs[bqidx + 3][0]
            ):
                bqidx += 4
                continue
            # unmatched double backquotes
            # if bqidx + 1 <= len(bqs) and \
            #    bqs[bqidx][0] + 1 ==  bqs[bqidx+1][0]:

            # :cmd:`some string`
            if bqidx > 0 and s[bqs[bqidx][0] - 1] == ':':
                bqidx += 2
                continue
            # `some <url>`_
            try:
                if bqidx + 1 < len(bqs) and s[bqs[bqidx + 1][0] + 1] == '_':
                    bqidx += 2
                    continue
            except IndexError:
                pass  # probably end of file
            self._ryd.name()
            if lnr != last_line_displayed:
                print(
                    '{}: {}'.format(lnr + self._line, s[lines[lnr] : lines[lnr + 1]]), end=""
                )

                last_line_displayed = lnr
            print(' ' * (-1 + len(str(lnr + self._line)) + bqs[bqidx][2]), '--^')
            bqidx += 1
        return False

    def rst2pdf(self, file_path: Union[Path, SysStdOut]) -> str:
        if self._ryd._args.verbose > 0:
            print('generating PDF')
        fn = str(file_path)
        return subprocess.check_output(
            ['rst2pdf', fn, '-s', 'freetype-sans,eightpoint'], encoding='utf-8'
        )

    def write(self) -> None:
        with self._out_path.open('w') as fp:
            try:
                self.dump(fp, base_dir=self._out_path.parent)
                rst_ok = True
            except RydExecError:
                rst_ok = False
        if not rst_ok:
            if self._ryd._args.keep:
                print('not removing partial', self._out_path)
            else:
                print('removing', self._out_path, 'add --keep to preserve partial result')
                self._out_path.unlink()
            sys.exit(1)

        if self._ryd._args.pdf is False:  # can be None
            return
        if self._ryd._args.pdf or self._md.get('pdf'):
            self.rst2pdf(self._out_path)
            if self._md.get('encrypt'):
                pw = self._md['encrypt']['passwd']
                # print('pw', pw, file=sys.stderr)
                assert isinstance(self._out_path, Path)
                pdf_file = self._out_path.with_suffix('.pdf')
                enc_file = self._out_path.with_suffix(
                    '.{:%Y%m%d}.pdf'.format(datetime.date.today())
                )
                # self._out_path.rename(tmp_file)
                subprocess.check_output(
                    ['pdftk', str(pdf_file), 'output', str(enc_file), 'user_pw', pw]
                )

    def dump(self, fp: Any = sys.stdout, base_dir: Optional[Path] = None) -> None:
        last_ended_in_double_colon = False
        last_code = False
        for d in self.data:
            # sys.stdout.flush()

            if hasattr(d, 'dump'):
                if not last_ended_in_double_colon and d.needs_double_colon:
                    print('\n::\n', file=fp)
                d.dump(fp, self)
                if hasattr(d, 'last_output'):
                    self.last_output = d.last_output
            elif isinstance(d, IncRaw):
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
                    print(p.read_text(), file=fp, end="")
            elif isinstance(d, Inc):
                if last_code:
                    last_code = False
                    print('', file=fp)
                for line in d.strip().splitlines():
                    if not line:
                        continue
                    if '{tempdir}' in line and line[0] != '/':
                        # is tempdir an instance?
                        raise NotImplementedError
                        # p = Path(line.format(tempdir=self.tempdir.directory))
                    elif base_dir is not None and line[0] != '/':
                        p = base_dir / line
                    else:
                        Path(line)
                    for line in p.open():
                        if line.strip():
                            print('  ', line, sep="", end="", file=fp)
                        else:
                            print('', line, sep="", end="", file=fp)
            # elif isinstance(d, PythonHidden):
            #    self.last_output = self.check_output(self.python_pre + d)
            #    if self.last_output is None:
            #        raise RydExecError("error executing Python")
            elif isinstance(d, (Python, PythonHidden)):
                if d and not isinstance(d, PythonHidden):
                    if not last_ended_in_double_colon:
                        print('\n.. code:: python\n', file=fp)
                    else:
                        print('should change :: to : before --- !python doc')
                    for line in d.strip().splitlines():
                        # print(' ', line, file=fp)
                        if line.strip():
                            print('  ', line, sep="", file=fp)
                        else:
                            print('', line, sep="", file=fp)
                    last_code = True
                else:
                    pass  # empty segment, might have pre-
                if isinstance(d, (Python, PythonHidden)):
                    self.last_output = self.check_output(self.python_pre + d)
                    if self._ryd._args.verbose > 1:
                        print('=========== output =========')
                        print(self.last_output, end="")
                        print('============================')
                    if self.last_output is None:
                        raise RydExecError('error executing Python')
            elif isinstance(d, (Code)):
                if d:
                    if not last_ended_in_double_colon:
                        print('\n::\n', file=fp)
                    for line in d.strip().splitlines():
                        # print(' ', line, file=fp)
                        if line.strip():
                            print('  ', line, sep="", file=fp)
                        else:
                            print('', line, sep="", file=fp)
                    last_code = True
            elif isinstance(d, PythonPre):
                self.python_pre = d
            elif isinstance(d, Comment):
                pass
            else:
                drs = str(d).rstrip()
                if drs.endswith('::'):
                    last_ended_in_double_colon = True
                    d = type(d)(drs + '\n\n')
                else:
                    last_ended_in_double_colon = False
                # the following forces an extra newline after code
                if last_code:
                    last_code = False
                    print('', file=fp)
                print(d, file=fp, end="")
                if isinstance(d, (Stdout, LastCompile, StdoutRaw)):
                    prefix = "" if isinstance(d, StdoutRaw) else '  '
                    op = self.last_compile if isinstance(d, LastCompile) else self.last_output
                    if op is None:
                        print(
                            '{}>>>>>>>>>  NO OUTPUT GENERATED <<<<<<<<<'.format(prefix),
                            file=fp,
                        )
                    else:
                        for line in op.rstrip().splitlines():
                            print('{}{}'.format(prefix, line), file=fp)
                    last_code = True
                elif type(d) != LiteralScalarString:
                    print('found unknown document type:', type(d))
                    try:
                        print('tag', d.tag)
                    except AttributeError:
                        pass
                    sys.exit(1)
