# coding: utf-8

from __future__ import annotations

import glob
import sys
import os
import io
import argparse
import subprocess
from inspect import stack, getframeinfo
from textwrap import dedent
from ruamel.std.pathlib import Path
import ruamel.yaml
from ruamel.yaml.split import YamlDocStreamSplitter, split

from typing import Any, Union, Optional, List, Tuple


Bugs = """\
- check empty documents. E.g. !python that only has code in !pre, and !stdout
  without any introductory text
"""

ToDo = """\
- some mechanism to show the name, leave option for 'skipping'/'converting'
  comment and push out newline later. Test incombination with verbosity
- specify Python interpreter, or create virtualenv + package installs, in a better
  way than using RYD_PYTHON env var.
- formalize temporary directory
- store (prefixed) program, only execute when !stdout is requested.
- parse messages like:
  README.rst:72: (ERROR/3) Inconsistent literal block quoting.
  and show output context
- zoom in on errors that have no line number: `some name <>`__
- document handling of :: in RST, and need for |+ in stdraw
- describe yaml comments after `|+ # `
- support code-block directive  http://rst2pdf.ralsina.me/handbook.html#syntax-highlighting
- list structure of the .ryd file
- process documents using xyz:prog  matching the document tag xyz by rt piping through prog
- why do toplevel LiteralScalarString dumps have |2, it is not even correct!
= consider moving to plugin system
"""


class RydExecError(Exception):
    pass


class RYD:
    def __init__(self, args: argparse.Namespace, config: Optional[Any] = None) -> None:
        self._args = args
        self._config = config
        self._name_printed = False
        self._current_path: Union[Path, None] = None

    def convert_subcommand(self) -> None:
        res = self.convert_all(self._args.file, verbose=self._args.verbose)
        if self._args.generate_mkdocs_config:
            self.generate_mkdocs_config(res, path=Path(self._args.generate_mkdocs_config))

    def generate_mkdocs_config(self, res: dict[Any, Any], path: Path) -> bool:
        for v in res.values():
            if 'mkdocs' in v[0]:
                self.yaml.dump(v[0]['mkdocs'], path)
                return True
        return False

    def convert_all(self, file_names: list[Any], verbose: int=0) -> dict[Any, Any]:
        ret_val = {}
        for file_name in file_names:
            self._name_printed = False
            if '*' in file_name or '?' in file_name:
                for exp_file_name in sorted(glob.glob(file_name)):
                    exp_path_name = Path(exp_file_name)
                    res = self.convert_one(exp_path_name, verbose=verbose)
                    ret_val[exp_path_name] = res
                continue
            path_name = Path(file_name)
            if path_name.is_dir():
                old_dir = os.getcwd()
                os.chdir(path_name)
                for ryd_name in Path('.').glob('*.ryd'):
                    res = self.convert_one(ryd_name, verbose=verbose)
                    ret_val[ryd_name] = res
                os.chdir(old_dir)
            else:
                res = self.convert_one(path_name, verbose=verbose)
                ret_val[path_name] = res
        # for k, v in ret_val.items():
        #    print(str(k), v)
        return ret_val

    def clean(self) -> None:
        for file_name in self._todo():
            self.convert_one(file_name, clean=True)

    def _todo(self) -> list[Path]:
        todo = []
        for file_name in self._args.file:
            self._name_printed = False
            if file_name[0] == '*':
                for exp_file_name in sorted(Path('.').glob(file_name)):
                    todo.append(exp_file_name)
                continue
            if '*' in file_name or '?' in file_name:
                for exp_file_name in sorted(glob.glob(file_name)):
                    todo.append(Path(exp_file_name))
                continue
            todo.append(Path(file_name))
        # print('todo', todo)
        return todo

    def name(self) -> None:
        """print name of file only once (either verbose or on error)"""
        if self._name_printed:
            return
        self._name_printed = True
        print(self._current_path)

    @property
    def yaml(self) -> ruamel.yaml.YAML:
        try:
            return self._yaml  # type: ignore
        except AttributeError:
            pass
        self._yaml = res = ruamel.yaml.YAML()
        return res

    def convert_one(
        self, path: Path, clean: bool = False, rt: bool = False, verbose: int = 0
    ) -> Union[Tuple[None, None], Tuple[dict[Any, Any], Path]]:
        sys.stdout.flush()
        if self._current_path is None and not path.exists():
            print('unknown command, or file:', path)
            sys.exit(1)
        self._current_path = path
        if verbose > 0:
            self.name()
        Conv: Any = None
        ys = YamlDocStreamSplitter(path, verbose=verbose)
        it = ys.iter()
        _, cx, sln = it.next(self.yaml)  # document metadata
        if 0.199 < float(cx['version']) < 0.201:
            if 'output' in cx:
                text = cx['output']
                print('should change "output: {text} in metadata to "text: {text}"')
            else:
                text = cx['text']
            if text == 'rst':
                from ryd._convertor.restructuredtext import RestructuredTextConvertor2 as Conv  # NOQA
            elif text == 'so':
                from ryd._convertor.stackoverflow import StackOverflowConvertor2 as Conv  # NOQA
            elif text == 'md':
                from ryd._convertor.markdown import MarkdownConvertor2 as Conv  # NOQA
        elif 0.099 < float(cx['version']) < 0.101:
            if cx['output'] == 'rst':
                from ryd._convertor.restructuredtext import RestructuredTextConvertor as Conv  # NOQA
            elif cx['output'] == 'md':
                from ryd._convertor.markdown import MarkdownConvertor as Conv  # NOQA
            elif cx['output'] == 'so':
                from ryd._convertor.stackoverflow import StackOverflowConvertor as Conv  # NOQA
            else:
                raise NotImplementedError
        assert Conv is not None
        convertor = Conv(self, self.yaml, cx, path)
        if clean:
            convertor.clean()
            return None, None
        if not convertor.check():
            return None, None
        docs_ok = True
        rt_ok = True
        while not it.done():
            y = it.next()
            # if y is None:
            #     break
            y, sln = y
            if not convertor.check_document(y, line=sln):
                docs_ok = False
                continue
            if not docs_ok:
                continue
            # print('yf', y)
            try:
                x = self.yaml.load(y)
            except Exception as e:
                raise
                if convertor.check_document(y, check_error=True, line=sln):
                    docs_ok = False
                else:
                    print(f'====== doc =====\n{y.decode("utf-8")}\n=======================')
                    print('exception', e)
                    raise  # no error_check succeeded
                docs_ok = False
            if rt:
                if not convertor.roundtrip(x, y):
                    rt_ok = False
                continue
            # print('x', repr(x))
            if not convertor(x):  # already up-to-date
                sys.stdout.flush()
                # ToDo you cannot return here, the PDF might not be generated because
                # of some rst2pdf issue
                return None, None
        if not docs_ok:
            return None, None
        if convertor.updated:
            if verbose > 0:
                print('updated')
        if rt:
            if rt_ok:
                convertor.roundtrip_write(path, self.yaml, cx)
            out_name = None
        else:
            out_name = convertor.write()
        return cx, out_name

    def from_rst(self) -> None:
        from .loadrst import LoadRST

        file_names = [Path(f) for f in self._args.file]
        if self._args.output and len(file_names) != 1:
            print('you can only have one argument if --output is set')
            return

        for file_name in file_names:
            ryd_name = Path(self._args.output) if self._args.output else file_name.with_suffix('.ryd')
            if ryd_name.exists() and not self._args.force:
                print('skipping', ryd_name)
                continue
            rst = LoadRST(file_name)
            rst.analyse_sections()
            print('writing', ryd_name)
            with ryd_name.open('w') as fp:
                fp.write(dedent("""\
                ---
                version: 0.2
                text: rst
                fix_inline_single_backquotes: true
                # post: pdf
                --- |
                """))  # NOQA
                fp.write(rst.update_sections())

    def roundtrip(self) -> None:
        for file_name in self._todo():
            self.convert_one(file_name, rt=True)

    def serve_subcommand(self) -> None:
        mkdocs_yaml = Path('.mkdocs.yaml')
        mkdocs_yaml_cleanup = False
        doc_path = Path('_doc')
        if doc_path.exists():
            res = self.convert_all([str(doc_path)], verbose=self._args.verbose)
            if not mkdocs_yaml.exists():
                mkdocs_yaml_cleanup = True
                if not self.generate_mkdocs_config(res, mkdocs_yaml):
                    print(f'did not generate {mkdocs_yaml}')
                    return
        cmd = ['mkdocs', 'serve', '-f', '.mkdocs.yaml', '--clean', '-t', 'readthedocs', '-v']
        os.system(' '.join(cmd))
        if mkdocs_yaml_cleanup:
            mkdocs_yaml.unlink()

    def rst_md(self) -> None:
        todo = list(self._todo())
        print('todo', todo)
        for expanded_path in todo:
            self.rst_md_one(Path(expanded_path), verbose=self._args.verbose)

    def rst_md_one(
        self, path: Path, *, verbose: int = 0,
    ) -> None:
        sys.stdout.flush()
        # if self._current_path is None and not path.exists():
        #     print('unknown command, or file:', path)
        #     sys.exit(1)
        self._current_path = path  # needed for self.name()
        if verbose > 0:
            self.name()
        yaml = ruamel.yaml.YAML()
        print('file', path.name)
        out = path # .with_suffix('.ryd.new')
        buf = io.BytesIO()
        pandoc = ['pandoc', '--from', 'rst', '--to', 'markdown']
        meta = True
        for doc, data, line_nr in split(path, yaml=yaml):
            if meta:
                meta = False
                assert data['text'] == 'rst'
                data['text'] = 'md'
                data['pdf'] = False
                try:
                    del data['fix_inline_single_backquotes']
                except KeyError:
                    pass
                yaml.dump(data, buf)
                continue
            # print(doc.decode('utf-8'), line_nr)
            tag = getattr(data, '_yaml_tag', None)
            # print(tag, type(doc), type(data), line_nr)
            if isinstance(data, ruamel.yaml.scalarstring.LiteralScalarString) and tag is None:
                # this is an non-tagged document, thus rst
                # print(repr(doc[:200]), line_nr)
                # print(doc.decode('utf-8')[:200], line_nr)
                # print(str(data)[:200], line_nr)
                # print(type(str(data)))
                res = subprocess.run(pandoc, input=str(data), encoding='utf-8', capture_output=True)
                buf.write(b'--- |\n')
                md_out = self.md_rewrite(res.stdout)
                # print(md_out[:200])
                buf.write(md_out.encode('utf-8'))
            else:
                buf.write(doc)
        out.write_bytes(buf.getvalue())

    def md_rewrite(self, s: str) -> str:
        return s

        # SPECIAL = '#*=+^"'
        # lines = s.splitlines()
        # for idx, line in enumerate(lines):
        #     if len(line) > 2 and line[0] in SPECIAL and line[0] == line[1] and line[0] == line[2]:
        #         try:
        #             underline, rest = line.split(None, 1)
        #         except:
        #             underline, rest = line, ''
        #         print('line', repr(underline), repr(rest))
        #         if idx + 1 < len(lines):
        #             if rest and lines[idx+1].startswith(underline):
        #                 lines[idx] = f'# {rest}'
        #                 lines[idx+1] = ''
        #                 continue
        # return '\n'.join(lines) + '\n'


