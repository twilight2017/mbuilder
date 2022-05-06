import os
import pathlib
import sys
from dataclasses import dataclass
from typing import Iterable, Tuple

import yaml
from dataclasses_json import dataclass_json
from loguru import logger
from git import Repo, InvalidGitRepositoryError

from .entity.repo_instance import RepoInstance
from .entity.version import Version

EXAMPLE_FILE = """
name: mes-backend
version: 0.1.0
key_file: ~/.ssh/id_rsa
image_folder: /root/service/images
prefix:mes-compose

repo_list:
  -name: backend
   folder: ./mes_backend
   hash: test
   image: app
   key: true
  -name: frontend
   folder: ./
   hash: test
   image: nginx
   key: true
"""

if not os.getenv("DEBUG", False):
    logger.add('info.log')


def get_current_repo() -> Repo:
    try:
        current_repo = Repo('.')  # 根据当前文件夹选择已有仓库
        return current_repo
    except InvalidGitRepositoryError:
        logger.error('not a vaild git repo')
        sys.exit(1)


current_repo = get_current_repo()


@dataclass_json
@dataclass
class Config:
    key_file: str
    image_folder: str
    prefix: str
    version: str
    repo_list: Tuple[RepoInstance]=(
        RepoInstance(floder="./mes-backend", hash="test", image="app", key=True),
        RepoInstance(floder="./", hash="test", image="nginx", key=False),
    )

    def get_image_list(self) -> Iterable[str]:
        for r in self.repo_list:
            yield r.image

    @staticmethod
    def gen():  # 生成config.yml
        path = './config.yml'
        logger.info(f'write tp {path}')
        p = pathlib.Path(path)
        with p.open('w'):
            p.write_text(EXAMPLE_FILE)

    @classmethod
    def load_config(cls) -> 'Config':
        config_path = pathlib.Path('./config.yml')  # 获取config.yml文件的路径
        if not config_path.exists():
            logger.critical('config.yml not exist. generate!')
            cls.gen()  # config.yml文件不存在时直接生成该文件
        with config_path.open() as f:
            data = yaml.load(f, Loader=yaml.FullLoader)  # 加载yaml文件,FullLoader参数代表加载完整的YAML语言。避免任意代码执行
        return Config.from_dict(data)

    def get_version(self) -> Version:
        return Version.parse_str(self.version)

    def get_prefix(self) -> str:
        """
        获取镜像的prefix
        :return:
        """
        return self.prefix

    def generate_image_version_path(self) -> pathlib.Path:
        """
        生成镜像+版本的路径
        :return:
        """
        image_path = pathlib.Path(f"{self.image_folder}/{self.get_version().get_full('_')}")  # 镜像文件夹和版本号进行拼接
        if not image_path.exists():
            image_path.mkdir()
        return image_path


CONFIG: Config = Config.load_config()
