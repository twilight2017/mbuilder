from git import Repo

from builder.core.conf import CONFIG  # CONFIG把所有的仓库带进来
from builder.core.entity.repo_instance import RepoInstance
from builder.core.error import BuilderError, HashInvaildError


class HashChecker:
    def __init__(self, repo:Repo):
        self.repo=repo

    '''
    静态方法是函数中的类，不需要实例，静态方法主要用来存放逻辑性的代码
    逻辑上属于类， 但是和类本身没有关系
    即，在静态方法中，不会涉及到类中的属性和方法的操作
    一言以蔽之，静态方法是个独立的、单纯的函数，只是把它放在了类中
    '''
    @staticmethod
    def check_equal(sub_r: Repo.submodules, config: RepoInstance):
        # 检查子模块hash和设置的hash值是否一致
        sub_hash = sub_r.module().head.commit
        if str(sub_hash) != config.hash:
            raise HashInvaildError

    def check_hash(self):
        """
        遍历仓库列表，查看Hash值是否都符合
        :return:
        """
        for sub_r in self.repo.submodules:
            find = False
            for config_r in CONFIG.repo_list:
                if sub_r.name == config_r.name:  # 子模块名称和仓库名称一致
                    find = True
                    self.check_equal(sub_r, config_r)
            if not find:
                raise BuilderError(f'submodule {sub_r.name} not found.')