#!/usr/bin/env python
from invoke import Context
from .conf import logger,CONFIG
from git import Repo


# repo is a Repo instance pointing to the git-python repository
def show_hash(repo: Repo):
    """
    展示子模块hash值
    :param repo:
    :return:
    """
    assert not repo.bare  # 仓库为空时抛出异常
    if not repo.submodules:
        logger.info("this repo has no submodules")
    for r in repo.submodules:
        logger.info(r.name+':'+str(r.module().head.commit))


def select_version():
    """
    调整子模块版本
    :return:
    """
    for repo in CONFIG.repo_list:
        c=Context()
        with c.cd(repo.floder):
            c.run(f"git reset --hard {repo.hash}")


if __name__ == '__main__':
    select_version()
