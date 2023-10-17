# coding: 'utf-8'

from __future__ import annotations

import subprocess
from ruamel.yaml import YAML
from ruamel.std.pathlib import Path
from ._base import ConvertorBase
from ryd.ryd import RYD

from typing import Dict, Any, List


class RoundTripConvertor(ConvertorBase):
    def __init__(self, ryd: RYD, yaml: YAML, md: Dict[str, Any], path: Path) -> None:
        super().__init__(ryd)
        self._yaml = yaml
        # for v in self._tag_obj.values():
        #     yaml.register_class(v)
        self._md = md
        self._path = path
        self._out_path = self._path  # .with_suffix('.ryd.new')
        self.data: List[Any] = [md]
        self.last_output = ""
        self.updated = False

    def __call__(self, x: Any) -> bool:
        print('>>>>>', x)
        if not self._ryd._args.oitnb:
            self.data.append(x)
            return True
        try:
            v = x.tag.value
        except AttributeError:
            self.data.append(x)
            return True
        if not v.startswith('!python') or not x.value.strip():
            self.data.append(x)
            return True
        # only python with a real body
        y = subprocess.check_output(
            ['oitnb', '-q', '-'], input=bytes(x.value, 'utf-8')
        ).decode('utf-8')
        if x.value != y:
            print(x.value, y)
            self.updated = True
            x.value = y + '\n'
        self.data.append(x)
        return True

    def write(self) -> None:
        print('writing')
        return
        self._yaml.explicit_start = True
        self._yaml.dump_all(self.data, self._out_path)
        # self._yaml.dump_all(self.data, sys.stdout)
