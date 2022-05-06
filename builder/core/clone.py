"""调用gitpython中的clone_from方法进行仓库clone"""
import pathlib
from git.repo import Repo


def clone(url, path:pathlib.Path) -> Repo:
    r = Repo.clone_from(url, path)
    return r
