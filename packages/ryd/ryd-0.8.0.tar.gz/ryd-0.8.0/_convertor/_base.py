# coding: utf-8

from __future__ import annotations

import os
import sys
import inspect
import importlib
import importlib.util
import subprocess
from textwrap import dedent
from typing import Optional, Any, Union, Dict, List, Tuple

from ruamel.yaml import YAML
from ruamel.std.pathlib import Path
import ruamel.std.pathlib.tempdir

from ryd.ryd import RYD
from ryd.classes_0_1 import RydDoc
from ryd.sys_stdout import SysStdOut


class ConvertorBase:
    def __init__(self, ryd: RYD) -> None:
        self._ryd = ryd
        self.updated = False
        # self.last_compile: Any = None
        self.last_source: Union[Path, None] = None
        self.last_output: Union[str, None] = None
        self.last_compile: Union[str, None] = None
        self._tempdir: Optional[ruamel.std.pathlib.tempdir.TempDir] = None
        self._tmpfile_nr = 0
        self._config_dir: Union[bool, None, Path] = False

    def __call__(self, s: Any) -> bool:
        """called for every loaded YAML doc, the first call normally
        tests if the output needs updating (i.e. based on timestamp)"""
        raise NotImplementedError

    def roundtrip(self, d: Any, src: bytes) -> bool:
        """"""
        raise NotImplementedError

    def clean(self) -> None:
        raise NotImplementedError

    def check(self) -> bool:
        # can be used to check if output is up-to-date
        return True

    def check_document(self, s: bytes, check_error: bool = False, line: int = -1) -> bool:
        def pr(*args: Any, s: Optional[str] = None, lnr: Optional[int] = None) -> None:
            if lnr is None:
                lnr = line
            if lnr > 0 and self._ryd._current_path is not None:
                print(f'{self._ryd._current_path.name}:{lnr} ->', end=' ')
            if args:
                print(*args)
            if s is not None:
                print('  line:', repr(s))

        # to check the document before loading
        fl, rest = s.split(b'\n', 1)
        while True:
            fls = fl.decode('utf-8')
            flss = fls.split()
            if not flss or flss[0][0] in '#%':
                fl, rest = rest.split(b'\n', 1)
            else:
                break
        if check_error:
            eck = False
            for x in flss[:3]:
                if x[0] == '|':
                    break
            else:
                pr('is there a missing "|"?', s=fls)
                print()
                eck = True
            return eck
        if len(flss) == 2 and flss[0] == '---' and flss[1][0] == '|':
            return True
        if len(flss) > 2 and flss[0] == '---' and flss[1][0] == '|' and flss[2][0] == '#':
            return True
        if len(flss) == 3 and flss[0] == '---' and flss[1][0] == '!' and flss[2][0] == '|':
            return True
        if (
            len(flss) > 3
            and flss[0] == '---'
            and flss[1][0] == '!'
            and flss[2][0] == '|'
            and flss[3][0] == '#'
        ):
            return True
        if not fls.startswith('---'):
            pr('expected doc to start with ---, got:', s=fls)
            return False
        if '!' in flss:
            pr('did you put a space between "!" and the tag?', s=fls)
            return False
        if flss == ['---']:
            pr('untagged root element detected did you forget " |" after "---"?', s=fls)
            return False
        return True

    def write(self) -> Any:
        raise NotImplementedError

    def add_text(self, s: str) -> None:
        raise NotImplementedError

    def add_code(self, s: str, typ: Optional[str] = None) -> None:
        raise NotImplementedError

    def add_last_output(self, typ: Optional[str] = None, raw: bool = False) -> None:
        raise NotImplementedError

    def add_last_compiler_output(self, typ: Optional[str] = None) -> None:
        raise NotImplementedError

    def add_table(self, s: Any) -> None:
        raise NotImplementedError

    def add_changelog(self, s: Any) -> None:
        raise NotImplementedError

    def check_output(
        self, s: str, exe: Optional[list[Any]] = None, ext: Optional[str] = None
    ) -> Union[str, None]:
        raise NotImplementedError

    @property
    def temp_dir(self) -> ruamel.std.pathlib.tempdir.TempDir:
        if self._tempdir is None:
            self._tempdir = ruamel.std.pathlib.tempdir.TempDir(prefix='ryd', keep=3)  # type: ignore
        return self._tempdir

    tempdir = temp_dir

    def temp_file_path(self, extension: str) -> Path:
        if len(extension) > 0 and extension[0] != '.':
            print(f'temp_file_path: extension should start with a "." ({extension})')
        p = self.temp_dir.directory / f'tmp_{self._tmpfile_nr:02d}{extension}'
        self.last_source = p
        self._tmpfile_nr += 1
        return p  # type: ignore

    @property
    def config_dir(self) -> Path | None:
        if self._config_dir is False:
            self._config_dir = None
            if self._ryd:
                try:
                    self._config_dir = self._ryd._config._path.parent  # type: ignore
                    if not self._config_dir.exists():  # type: ignore
                        self._config_dir = None
                except AttributeError:
                    pass
        assert not isinstance(self._config_dir, bool)
        return self._config_dir


class Convertor_0_1(ConvertorBase):
    """
    This first convertor assumes all known types are subclasses of RydDoc
    as avaliable in module ryd.ryd
    """

    def __init__(self, ryd: RYD) -> None:
        super().__init__(ryd)
        self._tag_obj: Dict[str, Any] = {}
        self._tag_doc = self.gather_tag_documentation()
        self.last_compile: Any = None
        self._path: Path
        self._out_path: Union[Path, SysStdOut]

    def gather_tag_documentation(self) -> Dict[str, List[Any]]:
        tag_doc = {}
        for _name, obj in inspect.getmembers(sys.modules['ryd.classes_0_1']):
            if (
                inspect.isclass(obj)
                and obj is not RydDoc
                and issubclass(obj, RydDoc)
                and hasattr(obj, 'yaml_tag')
            ):
                self._tag_obj[obj.yaml_tag] = obj
                d = obj.__doc__ if obj.__doc__ is not None else 'N/A\n  N/A'
                d1, d2 = d.lstrip().split('\n', 1)
                d1 = d1.strip()
                d2 = dedent(d2).lstrip()
                tag_doc[obj.yaml_tag] = [d1, d2]
        return tag_doc

    def get_tags(self) -> Dict[str, List[Any]]:
        return self._tag_doc

    def update(self, s: Any) -> Any:
        return s

    def clean(self) -> None:
        assert self._path.exists()
        if self._out_path.exists():
            self._out_path.unlink()

    python_exe = os.environ.get('RYD_PYTHON', sys.executable)
    # print('python_exe', python_exe, sys.executable)

    def check_output(
        self, s: str, exe: Optional[list[Any]] = None, ext: Optional[str] = None
    ) -> Union[str, None]:
        if exe is None:
            exe = [self.python_exe, None]
            ext = '.py'
        if ext is None:
            raise NotImplementedError
        p = self.temp_dir.directory / 'tmp_{}{}'.format(self._tmpfile_nr, ext)
        self.last_source = p
        self._tmpfile_nr += 1
        p.write_text(s)
        try:
            return subprocess.check_output(
                [x if x is not None else str(p) for x in exe],
                stderr=subprocess.STDOUT,
                encoding='utf-8',
            )
        except subprocess.CalledProcessError as e:  # NOQA
            sys.stdout.write(e.output)
            if 'ImportError: No module named ryd.ryd' in e.output:
                print(
                    '\nWhen generating ryd documentation use:\n'
                    '  RYD_PYTHON=/opt/util/ryd/bin/python ryd ...'
                )
            return None


class Convertor_0_2(ConvertorBase):
    """
    This first convertor assumes all known types are subclasses of RydDoc
    as avaliable in module ryd.ryd
    """

    def __init__(self, ryd: RYD, yaml: YAML, md: Dict[str, Any], path: Path) -> None:
        super().__init__(ryd)
        self._yaml = yaml
        self._md = md
        self._path = path
        self.instances: Dict[str, Any] = {}
        self.start_line = [0]
        self.input: List[Any] = []

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._md

    def __call__(self, s: Any, line_nr: Optional[int] = None) -> bool:
        """input appending no processing"""
        self.input.append(s)
        self.start_line.append(str(s).count('\n'))
        return True

    python_exe = os.environ.get('RYD_PYTHON', sys.executable)

    def check_output(
        self, s: str, exe: Optional[list[Any]] = None, ext: Optional[str] = None
    ) -> Union[str, None]:
        """ToDo: this should probably go to programbase and use subprocess.run """
        if exe is None:
            exe = [self.python_exe, None]
            ext = '.py'
        if ext is None:
            raise NotImplementedError
        self.last_source = p = self.temp_file_path(ext)
        p.write_text(s)
        cmd = [str(x) if x is not None else str(p) for x in exe]
        try:
            return subprocess.check_output(cmd, stderr=subprocess.STDOUT, encoding='utf-8',)
        except subprocess.CalledProcessError as e:  # NOQA
            sys.stdout.write(e.output)
            if 'ImportError: No module named ryd.ryd' in e.output:
                print(
                    '\nWhen generating ryd documentation use:\n'
                    '  RYD_PYTHON=/opt/util/ryd/bin/python ryd ...'
                )
            return None

    def get_tag(self, tagged_scalar: Any) -> Tuple[str, Union[str, None]]:
        full_tag: str = tagged_scalar.tag.trval.lstrip('!')
        if '-' in full_tag:
            return full_tag.split('-', 1)  # type: ignore
        return full_tag, None

    def get_instance(self, tag: str) -> Any:
        """ should probably scan all files in _tag and preload"""
        if tag not in self.instances:
            if self.config_dir:
                fn = self.config_dir / 'tag' / f'{tag}.py'
                if fn.exists():
                    spec = importlib.util.spec_from_file_location(tag, fn)
                    assert spec is not None
                    assert spec.loader is not None
                    mytag = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mytag)
                    cls = getattr(mytag, tag.capitalize())
                    self.instances[tag] = t = cls(self)
                    return t
            try:
                cls = getattr(importlib.import_module(f'ryd._tag.{tag}'), tag.capitalize())
                # hand in the convertor for setting/getting information between documents
                self.instances[tag] = cls(self)
            except Exception as e:
                print(e)
                print('tag', tag.capitalize())
                raise
        return self.instances[tag]

    def get_all_tags(self) -> Dict[str, Any]:
        # derived from https://stackoverflow.com/questions/40008155
        def get_subclass_methods(cls: Any) -> List[str]:
            methods = set([d for d in dir(cls) if d[0] != '_'])
            unique_methods = methods.difference(*(dir(base) for base in cls.__bases__))
            return sorted(unique_methods)

        tag_dir = Path(__file__).parent.parent / '_tag'
        tag_doc = {}
        for fn in tag_dir.glob('*.py'):
            if fn.name.startswith('_'):
                continue
            tag = fn.stem
            import_name = 'ryd.' + str(fn).split('/ryd/', 1)[1].replace('/', '.')[:-3]
            # print(import_name)
            cls = getattr(importlib.import_module(import_name), tag.capitalize())
            md = cls.__call__.__doc__ if cls.__call__.__doc__ is not None else 'N/A\n  N/A'
            d1, d2 = md.lstrip().split('\n', 1)
            d1 = d1.strip()
            d2 = dedent(d2).lstrip()
            tag_doc['!' + tag] = [d1, d2]
            for name in get_subclass_methods(cls):
                d = getattr(cls, name).__doc__
                if d is None:
                    continue
                d1, d2 = md.lstrip().split('\n', 1)
                d1 = d1.strip()
                d2 = dedent(d2).lstrip()
                tag_doc[f'!{tag}-{name}'] = [d1, d2]
        return tag_doc
