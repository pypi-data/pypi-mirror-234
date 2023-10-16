"""
This is a module that will install OS packages for you.
"""


from typing import List
import os

from pydmt.utils.filesystem import unlink_files, mkdir_touch
from pydmt.configs import ConfigSudo, ConfigApt
from pydmt.utils.subprocess import check_call

from pydmt.api.one_source_one_target import OneSourceOneTarget


class BuilderApt(OneSourceOneTarget):
    def __init__(self, source: str, target: str, packages: List[str]):
        super().__init__(source, target)
        self.packages = packages

    def build(self) -> None:
        unlink_files([self.target])
        if not self.packages:
            mkdir_touch(self.target)
            return
        os.environ['DEBIAN_FRONTEND'] = 'noninteractive'
        args = []
        if ConfigSudo.sudo:
            args.append("sudo")
        args.extend([
            'apt-get',
        ])
        if ConfigApt.apt_quiet:
            args.append("-q=2")
        args.extend([
            '--yes',
            'update',
        ])
        check_call(args)
        args = []
        if ConfigSudo.sudo:
            args.append("sudo")
        args.extend([
            'apt-get',
        ])
        if ConfigApt.apt_quiet:
            args.append("-q=2")
        args.extend([
            '--yes',
            'install',
        ])
        args.extend(self.packages)
        check_call(args)
        mkdir_touch(self.target)
