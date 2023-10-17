# coding: utf-8

import sys
from typing import Any, Union, Dict, Set, List

from ruamel.std.pathlib import Path


class LoadRST:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._lines: Union[List[str], None] = None
        self._blank = set([-1])  # in case you have a divider on the first line
        self._section_lines: Dict[int, str] = {}
        self._divider_lines: Set[Any] = set()
        self._double_section = ""  # above and below
        self._double_section_lines: Dict[Any, Any] = {}
        self._single_section = ""  # only below
        self._single_section_lines: Dict[Any, Any] = {}

    @property
    def lines(self) -> list[str]:
        if self._lines is None:
            self._lines = self._path.read_text().splitlines()
        assert isinstance(self._lines, list)
        return self._lines

    def analyse_sections(self) -> None:
        non_alpha = '\'"#*=-^+'
        non_alpha = '=-`:\'"~^_*+#<>.'

        def char_repeats(line: str) -> bool:
            """assume a stripped line, check if the first character is repeated"""
            idx = len(line)
            while idx > 1:
                idx -= 1
                if line[idx] != line[0]:
                    return False
            return True

        # for x in ['===', '==', '=', 'x=']:
        #    print(x, char_repeats(x))
        current_level = 0  # NOQA
        previous_blank = False  # NOQA
        for line_number, line in enumerate(self.lines):
            s_line = line.strip()
            if not s_line:
                self._blank.add(line_number)
                previous_blank = True
                continue  # empty line
            fc = line[0]  # first character
            if fc not in non_alpha or not char_repeats(s_line):
                previous_blank = False  # NOQA
                continue
            self._section_lines[line_number] = s_line
        # print(self._blank)
        for line_number in self._section_lines:
            if (line_number - 1) in self._blank and (line_number + 1) in self._blank:
                self._divider_lines.add(line_number)
        for line_number in self._divider_lines:
            del self._section_lines[line_number]
        # cleaned up, now analyse
        line_numbers = sorted(self._section_lines.keys())
        idx = -1
        single_level = 0
        while idx < len(line_numbers) - 1:
            idx += 1
            line_number = line_numbers[idx]
            line = self._section_lines[line_number]
            # print(line_number, self._section_lines[line_number])
            if line_number + 2 in self._section_lines:
                if line[0] == self._section_lines[line_number + 2][0]:
                    pass
                    # print('double', line_number)
                else:
                    print('non-matching over-under-line', line_number)
                    sys.exit(1)
                idx += 1  # skip the matching underline
                if not self._double_section and self._single_section:
                    print("don't know how to handle over-under-line after under-line")
                    sys.exit(1)
                if line[0] not in self._double_section:
                    self._double_section += line[0]
                self._double_section_lines.setdefault(line[0], []).extend(
                    [line_number, line_number + 2]
                )
                single_level = 0
                continue
            if line[0] not in self._single_section:
                if single_level != len(self._single_section):
                    print('unexpected underline level', line_number, single_level)
                    sys.exit(1)
                self._single_section += line[0]
                single_level += 1
            else:
                single_level = self._single_section.index(line[0]) + 1
            self._single_section_lines.setdefault(line[0], []).append(line_number)

        print('double:', self._double_section)
        print('       ', self._double_section_lines)
        print('single:', self._single_section)
        print('       ', self._single_section_lines)

    def update_sections(self) -> str:
        # almost the Python recomendation, but not using '-' for sections, as
        # that can cause problems with YAML document markers
        double = '#*'
        single = '=+^"'
        assert len(double) >= len(self._double_section)
        assert len(single) >= len(self._single_section)
        for level, ch in enumerate(self._double_section):
            new_ch = double[level]
            for line_number in self._double_section_lines[ch]:
                self.lines[line_number] = new_ch * len(self.lines[line_number])
        for level, ch in enumerate(self._single_section):
            new_ch = single[level]
            for line_number in self._single_section_lines[ch]:
                self.lines[line_number] = new_ch * len(self.lines[line_number])
        return '\n'.join(self.lines) + '\n'
