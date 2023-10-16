from pydmt.api.feature import Feature
from pydmt.builders.apt import BuilderApt
from pydmt.core.pydmt import PyDMT
from pydmt.helpers.urls import get_deps


class FeatureApt(Feature):
    def __init__(
        self,
    ):
        self.packages = get_deps()

    def setup(self, pydmt: PyDMT) -> None:
        if self.packages is not None:
            pydmt.add_builder(BuilderApt(
                source="config/deps.py",
                target="out/deps.stamp",
                packages=self.packages
            ))
