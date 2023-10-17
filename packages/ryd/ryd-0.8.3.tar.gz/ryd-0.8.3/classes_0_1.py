# coding: utf-8

from __future__ import annotations

import subprocess
from ruamel.yaml.scalarstring import LiteralScalarString

from typing import Any, Union, TextIO, TYPE_CHECKING

if TYPE_CHECKING:
    from ._convertor._base import ConvertorBase


class RydDoc(LiteralScalarString):

    needs_double_colon = True

    @classmethod
    def from_yaml(cls, constructor: Any, node: Any) -> Any:
        return cls(node.value)

    @classmethod
    def to_yaml(cls, representer: Any, node: Any) -> Any:
        return representer.represent_literal_scalarstring(cls.yaml_tag, node.value)  # type: ignore # NOQA


# class BashRaw(RydDoc):
#     """Invoke bash on the document as script.
#     """
#     yaml_tag = '!bash-raw'


class Code(RydDoc):
    """Include program in text. Do not mark as executable, doesn't influence \
   ``!stdout``.
    """

    yaml_tag = '!code'


class Comment(RydDoc):
    """The whole document will be discarded, i.e. not included in the output.

    This allows commenting out complete sections in an output independent way.
    """

    yaml_tag = '!comment'


class Inc(RydDoc):
    """Include the content of the listed files (indented), without other processing, \
    into the output. Preceed with ``::`` if necessary.

    If a file name doesn't start with ``/``, it is considered to be relative to the
    directory of the output path.
    """

    yaml_tag = '!inc'


class IncRaw(RydDoc):
    """Include the listed files raw (i.e. without processing, or indenting) into the output.

    If a file name doesn't start with ``/``, it is considered to be relative to the
    directory of the output path.
    """

    yaml_tag = '!incraw'


class LastCompile(RydDoc):
    """Include output from last compilation as code.

    """

    yaml_tag = '!last-compile'


class Python(RydDoc):
    """Include Python program in text. Prefix and mark as executable.
    """

    yaml_tag = '!python'


class PythonHidden(RydDoc):
    '''Do  not include Python program in text. Prefix and mark as executable.

    This can be used to write files to the output directory, using:
    import pathlib; pathlib.Path("file_name").writetext("""contents of file""")
    '''

    yaml_tag = '!python-hidden'


class PythonPre(RydDoc):
    """Prefix all following ``!python`` documents with this document (e.g. used for imports)

    This part will not be be shown. The content should be a python snippet, that
    will be used as prefix for following programs which can be incomplete.
    This is useful for  suppressing repetetive import statements.
    """

    yaml_tag = '!python-pre'


class Stdout(RydDoc):
    """Include output from last executable document (e.g. ``!python``) as code.

    """

    yaml_tag = '!stdout'


class StdoutRaw(RydDoc):
    """
    Include output from the last program, as source for the output format.

    This can be used to e.g. have a program generate an definition list programmatically.
    """

    yaml_tag = '!stdout-raw'


class RydProgram(RydDoc):
    needs_double_colon = True

    def dump(self, fp: TextIO, convertor: ConvertorBase) -> None:
        """generic include of code with indentation unless empty"""
        for line in self.strip().splitlines():
            if line.strip():
                print('  ', line, sep="", file=fp)
            else:
                print('', line, sep="", file=fp)
        print(file=fp)
        # convertor.last_code = True
        # not using nim prefix when unpy-ing
        self.last_output = self.check_output(convertor)

    def check_output(self, convertor: ConvertorBase) -> Union[str, None]:
        raise NotImplementedError


#########
# Nim
#########
class Nim(RydProgram):
    """Include Nim program in text. Prefix and mark as executable.
    """

    yaml_tag = '!nim'

    def check_output(self, convertor: ConvertorBase) -> Union[str, None]:
        # None is replaced by the filename
        cmd = ['nim', 'compile', '--verbosity:0', '--hint[Processing]:off', None]
        convertor.last_compile = convertor.check_output(
            convertor.nim_pre + self,  # type: ignore
            exe=cmd,
            ext='.nim',
        )
        # print('convertor.last_compile', convertor.last_compile)
        assert convertor.last_source is not None
        exe = convertor.last_source.with_suffix("")
        if exe.exists():
            return subprocess.check_output([exe]).decode('utf-8')
        return convertor.last_compile


class NimPre(RydDoc):
    """Prefix all following ``!nim`` documents with this document (e.g. used for imports)

    This part will not be be shown. The content should be a nim snippet, that
    will be used as prefix for following programs which can be incomplete.
    This is useful for  suppressing repetetive import statements.
    """

    yaml_tag = '!nim-pre'

    def dump(self, fp: Any, convertor: ConvertorBase) -> None:
        convertor.nim_pre = self  # type: ignore


class UnPy(RydProgram):
    """Include Nim program in text. Do not mark as executable. Set output to result of unpy.
    """

    yaml_tag = '!unpy'

    def check_output(self, convertor: ConvertorBase) -> Union[str, None]:
        # None is replaced by the filename
        return convertor.check_output(
            self, exe=['unpy', 'update', '--output:-', None], ext='.nim'
        )
