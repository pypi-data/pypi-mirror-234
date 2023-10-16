# coding: utf-8
# flake8: noqa
# cligen: 0.3.2, dd: 2023-10-10, args: gen


import argparse
import importlib
import os
import pathlib
import ruamel.yaml
import sys
import typing

from . import __version__


class HelpFormatter(argparse.RawDescriptionHelpFormatter):
    def __init__(self, *args: typing.Any, **kw: typing.Any):
        kw['max_help_position'] = 40
        super().__init__(*args, **kw)

    def _fill_text(self, text: str, width: int, indent: str) -> str:
        import textwrap

        paragraphs = []
        for paragraph in text.splitlines():
            paragraphs.append(textwrap.fill(paragraph, width,
                             initial_indent=indent,
                             subsequent_indent=indent))
        return '\n'.join(paragraphs)


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args: typing.Any, **kw: typing.Any):
        kw['formatter_class'] = HelpFormatter
        super().__init__(*args, **kw)


class DefaultVal(str):
    def __init__(self, val: typing.Any):
        self.val = val

    def __str__(self) -> str:
        return str(self.val)


class ConfigBase:
    suffix = ""

    def __init__(self, path: typing.Optional[typing.Union[pathlib.Path, str]]=None):
        self._data = None
        tmp_path = self.get_config_parm()
        if tmp_path:
            self._path = tmp_path
        elif isinstance(path, pathlib.Path):
            self._path = path
        elif path is not None:
            if path[0] in '~/':
                self._path = pathlib.Path(path).expanduser()
            elif '/' in path:  # assume '!Config config_dir/config_name'
                self._path = self.config_dir / path
            else:
                self._path = self.config_dir / path / (path.rsplit('.')[-1] + self.suffix)
        else:
            raise NotImplementedError

    @property
    def data(self) -> typing.Any:
        if self._data is None:
            self._data = self.load()  # NOQA
        return self._data

    def get(self, *args: typing.Any, pd: typing.Optional[typing.Any]=None) -> typing.Any:
        data = self.data
        try:
            for arg in args:
                if arg in data:
                    data = data[arg]
                else:
                    break
            else:
                return data
        except Exception as e:
            print(f'exception getting "{arg}" from "{args}" ({self.data})') 
            return {}
        if args[0] != 'global':
            return self.get(*(['global'] + list(args[1:])), pd=pd)
        return pd

    def get_config_parm(self) -> typing.Union[pathlib.Path, None]:
        for idx, arg in enumerate(sys.argv[1:]):
            if arg.startswith('--config'):
                if len(arg) > 8 and arg[8] == '=':
                    return pathlib.Path(arg[9:])
                else:
                    try:
                        return pathlib.Path(sys.argv[idx + 2])
                    except IndexError:
                        print('--config needs an argument')
                        sys.exit(1)
        return None

    @property
    def config_dir(self) -> pathlib.Path:
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            if sys.platform.startswith('win32'):
                d = os.environ['APPDATA']
            else:
                d = os.environ.get(
                    'XDG_CONFIG_HOME', os.path.join(os.environ['HOME'], '.config')
                )
            pd = pathlib.Path(d)
            setattr(self, attr, pd)
            return pd
        return getattr(self, attr)  # type: ignore

    def load(self) -> typing.Any:
        raise NotImplementedError


class ConfigYAML(ConfigBase):
    suffix = '.yaml'

    def load(self) -> typing.Any:
        yaml = ruamel.yaml.YAML(typ='safe')
        try:
            data = yaml.load(self._path)
        except (FileNotFoundError, TypeError, KeyError):
            return {}
        return data

    def __repr__(self) -> str:
        return f'ConfigYAML(path="{self._path}")'


class CountAction(argparse.Action):

    def __call__(
        self,
        parser: typing.Any,
        namespace: argparse.Namespace,
        values: typing.Union[str, typing.Sequence[str], None],
        option_string: typing.Optional[str] = None,
    ) -> None:
        if self.const is None:
            self.const = 1
        try:
            val = getattr(namespace, self.dest) + self.const
        except TypeError:  # probably None
            val = self.const
        setattr(namespace, self.dest, val)


def main(cmdarg: typing.Optional[typing.List[str]]=None) -> int:
    cmdarg = sys.argv if cmdarg is None else cmdarg
    parsers = []
    config = ConfigYAML(path='ryd')
    parsers.append(ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, epilog='Sections, subsections, etc. in .ryd files\n  # with over-line, for parts\n  * with over-line, for chapters\n  =, for sections\n  +, for subsections\n  ^, for subsubsections\n  ", for paragraphs\n'))
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(config.get('global', 'verbose', pd=0)), dest='_gl_verbose', metavar='VERBOSE', nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--force', default=DefaultVal(config.get('global', 'force', pd=0)), dest='_gl_force', metavar='FORCE', nargs=0, help='force action, even on normally skipped files', action=CountAction, const=1)
    parsers[-1].add_argument('--version', action='store_true', help='show program\'s version number and exit')
    subp = parsers[-1].add_subparsers()
    px = subp.add_parser('convert', help='generate output as per first YAML document')
    px.set_defaults(subparser_func='convert')
    parsers.append(px)
    parsers[-1].add_argument('--pdf', default=config.get('convert', 'pdf', pd=None), action='store_true', help='postprocess to pdf')
    parsers[-1].add_argument('--no-pdf', default=config.get('convert', 'no_pdf', pd=False), action='store_false', dest='pdf')
    parsers[-1].add_argument('--html', default=config.get('convert', 'html', pd=None), action='store_true', help='postprocess to HTML')
    parsers[-1].add_argument('--no-html', default=config.get('convert', 'no_html', pd=False), action='store_false', dest='html')
    parsers[-1].add_argument('--embed', default=config.get('convert', 'embed', pd=False), action='store_true', help='embed images in HTML')
    parsers[-1].add_argument('--stdout', default=config.get('convert', 'stdout', pd=False), action='store_true', help='write to stdout instead of file')
    parsers[-1].add_argument('--keep', default=config.get('convert', 'keep', pd=False), action='store_true', help='preserve partial .rst/.md on execution error')
    parsers[-1].add_argument('--generate-mkdocs-config', default=config.get('convert', 'generate_mkdocs_config', pd=None), help='generate the config file for mkdocs from metadata')
    parsers[-1].add_argument('file', nargs='+' if config.get('convert', 'file', pd=None)==None else '*', default=config.get('convert', 'file', pd=None), help='files to process')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(config.get('convert', 'verbose', pd=0)), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--force', default=DefaultVal(config.get('convert', 'force', pd=0)), nargs=0, help='force action, even on normally skipped files', action=CountAction, const=1)
    px = subp.add_parser('clean', help='clean output files for .ryd files')
    px.set_defaults(subparser_func='clean')
    parsers.append(px)
    parsers[-1].add_argument('file', nargs='+' if config.get('clean', 'file', pd=None)==None else '*', default=config.get('clean', 'file', pd=None), help='files to process')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(config.get('clean', 'verbose', pd=0)), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--force', default=DefaultVal(config.get('clean', 'force', pd=0)), nargs=0, help='force action, even on normally skipped files', action=CountAction, const=1)
    px = subp.add_parser('roundtrip', help='roundtrip .ryd file, updating sections')
    px.set_defaults(subparser_func='roundtrip')
    parsers.append(px)
    parsers[-1].add_argument('file', nargs='+' if config.get('roundtrip', 'file', pd=None)==None else '*', default=config.get('roundtrip', 'file', pd=None), help='files to process')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(config.get('roundtrip', 'verbose', pd=0)), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--force', default=DefaultVal(config.get('roundtrip', 'force', pd=0)), nargs=0, help='force action, even on normally skipped files', action=CountAction, const=1)
    px = subp.add_parser('from-rst', help='convert .rst to .ryd with some section anylysis')
    px.set_defaults(subparser_func='from_rst')
    parsers.append(px)
    parsers[-1].add_argument('--output', '-o', default=config.get('from-rst', 'output', pd=None), help='write to file (default argument with .ryd suffix)')
    parsers[-1].add_argument('file', nargs='+' if config.get('from-rst', 'file', pd=None)==None else '*', default=config.get('from-rst', 'file', pd=None), help='files to process')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(config.get('from-rst', 'verbose', pd=0)), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--force', default=DefaultVal(config.get('from-rst', 'force', pd=0)), nargs=0, help='force action, even on normally skipped files', action=CountAction, const=1)
    px = subp.add_parser('rst-md', help='convert .ryd file from reST content to markdown  content')
    px.set_defaults(subparser_func='rst_md')
    parsers.append(px)
    parsers[-1].add_argument('file', nargs='+' if config.get('rst-md', 'file', pd=None)==None else '*', default=config.get('rst-md', 'file', pd=None), help='files to process')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(config.get('rst-md', 'verbose', pd=0)), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--force', default=DefaultVal(config.get('rst-md', 'force', pd=0)), nargs=0, help='force action, even on normally skipped files', action=CountAction, const=1)
    px = subp.add_parser('serve', help='use mkdocs serve -f .mkdocs.yaml to serve .md files')
    px.set_defaults(subparser_func='serve')
    parsers.append(px)
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(config.get('serve', 'verbose', pd=0)), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--force', default=DefaultVal(config.get('serve', 'force', pd=0)), nargs=0, help='force action, even on normally skipped files', action=CountAction, const=1)
    parsers.pop()
    # sp: convert
    _subparser_found = False
    for arg in cmdarg[1:]:
        if arg in ['-h', '--help', '--version']:  # global help if no subparser
            break
    else:
        end_pos = None if '--' not in cmdarg else cmdarg.index('--')
        for sp_name in ['convert', 'clean', 'roundtrip', 'from-rst', 'rst-md', 'serve']:
            if sp_name in cmdarg[1:end_pos]:
                break
        else:
            # insert default in first position, this implies no
            # global options without a sub_parsers specified
            cmdarg.insert(1, 'convert')
    if '--version' in cmdarg[1:]:
        if '-v' in cmdarg[1:] or '--verbose' in cmdarg[1:]:
            return list_versions(pkg_name='ryd', version=None, pkgs=['ruamel.std.pathlib', 'ruamel.yaml'])
        print(__version__)
        return 0
    if '--help-all' in cmdarg[1:]:
        try:
            parsers[0].parse_args(['--help'])
        except SystemExit:
            pass
        for sc in parsers[1:]:
            print('-' * 72)
            try:
                parsers[0].parse_args([sc.prog.split()[1], '--help'])
            except SystemExit:
                pass
        sys.exit(0)
    args = parsers[0].parse_args(args=cmdarg[1:])
    for gl in ['verbose', 'force']:
        glv = getattr(args, '_gl_' + gl, None)
        if isinstance(getattr(args, gl, None), (DefaultVal, type(None))) and glv is not None:
            setattr(args, gl, glv)
        delattr(args, '_gl_' + gl)
        if isinstance(getattr(args, gl, None), DefaultVal):
            setattr(args, gl, getattr(args, gl).val)
    cls = getattr(importlib.import_module('ryd.ryd'), 'RYD')
    obj = cls(args, config=config)
    funcname = getattr(args, 'subparser_func', None)
    if funcname is None:
        parsers[0].parse_args(['--help'])
    fun = getattr(obj, funcname + '_subcommand', None)  # type: ignore
    if fun is None:
        fun = getattr(obj, funcname)  # type: ignore
    ret_val = fun()
    if ret_val is None:
        return 0
    if isinstance(ret_val, int):
        return ret_val
    return -1

def list_versions(pkg_name: str, version: typing.Union[str, None], pkgs: typing.Sequence[str]) -> int:
    version_data = [
        ('Python', '{v.major}.{v.minor}.{v.micro}'.format(v=sys.version_info)),
        (pkg_name, __version__ if version is None else version),
    ]
    for pkg in pkgs:
        try:
            version_data.append(
                (pkg,  getattr(importlib.import_module(pkg), '__version__', '--'))
            )
        except ModuleNotFoundError:
            version_data.append((pkg, 'NA'))
        except KeyError:
            pass
    longest = max([len(x[0]) for x in version_data]) + 1
    for pkg, ver in version_data:
        print('{:{}s} {}'.format(pkg + ':', longest, ver))
    return 0


if __name__ == '__main__':
    sys.exit(main())
