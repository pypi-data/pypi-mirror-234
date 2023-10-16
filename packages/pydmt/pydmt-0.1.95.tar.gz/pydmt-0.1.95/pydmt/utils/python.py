import os
import glob
import pprint
from typing import List
import importlib

from pydmt.configs import ConfigTarget


def hlp_source_under(folder):
    """
    this function finds all the python packages under a folder and
    write the 'packages' and 'package_dir' entries for a python setup.py
    script
    """
    # walk the folder and find the __init__.py entries for packages.
    packages = []
    package_dir = {}
    for root, _, files in os.walk(folder):
        for file in files:
            if file != '__init__.py':
                continue
            full = os.path.dirname(os.path.join(root, file))
            relative = os.path.relpath(full, folder)
            packages.append(relative)
            package_dir[relative] = full
    # we use pprint because we want the order to always remain the same
    return f"packages={sorted(packages)},\npackage_dir={pprint.pformat(package_dir)}"


def hlp_files_under(destination_folder, pat):
    file_list = [x for x in glob.glob(pat) if os.path.isfile(x)]
    return f"('{destination_folder}', {file_list})"


def make_hlp_project_keywords(d):
    def hlp_project_keywords():
        return f"{d.project_keywords.split()}"

    return hlp_project_keywords


def make_hlp_project_platforms(d):
    def hlp_project_platforms():
        return f"{d.project_platforms.split()}"

    return hlp_project_platforms


def make_hlp_project_classifiers(d):
    def hlp_project_classifiers():
        classifiers = d.project_classifiers.split('\n')
        classifiers = [x.strip()[1:-1] for x in classifiers]
        return f"{classifiers}"

    return hlp_project_classifiers


def make_hlp_wrap(level):
    def hlp_wrap(t):
        return t.replace('\n', '\n' + '\t' * level)

    return hlp_wrap


def collect_reqs() -> List[str]:
    collect = []
    mod = importlib.import_module("config.python")
    if hasattr(mod, "dev_requires") and ConfigTarget.dev:
        collect.extend(getattr(mod, "dev_requires"))
    if hasattr(mod, "test_requires"):
        collect.extend(getattr(mod, "test_requires"))
    if hasattr(mod, "install_requires"):
        collect.extend(getattr(mod, "install_requires"))
    if hasattr(mod, "config_requires"):
        collect.extend(getattr(mod, "config_requires"))
    if hasattr(mod, "setup_requires"):
        collect.extend(getattr(mod, "setup_requires"))
    if hasattr(mod, "make_requires"):
        collect.extend(getattr(mod, "make_requires"))
    return collect


def collect_bootstrap_reqs() -> List[str]:
    try:
        mod = importlib.import_module("config.bootstrap")
        if hasattr(mod, "requires"):
            return getattr(mod, "requires")
    except ModuleNotFoundError:
        pass
    return []


def get_install_args():
    return [
        "python",
        "-m",
        "pip",
        "install",
    ]
