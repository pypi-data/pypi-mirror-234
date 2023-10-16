"""
This module runs make
"""


from pydmt.utils.filesystem import mkdir_touch
from pydmt.utils.subprocess import check_call_ve

from pydmt.api.one_source_one_target import OneSourceOneTarget

from pydmt.configs import ConfigTarget

SOURCE_FILE = "Makefile"


class BuilderMake(OneSourceOneTarget):
    def build(self) -> None:
        args = [
            "make",
        ]
        if not ConfigTarget.dev:
            args.append("DEV=0")
        check_call_ve(args)
        mkdir_touch(self.target)
