import click
from .core.conf import CONFIG, current_repo
from loguru import logger
from .core.version import show_hash
from .core.hash_checker import HashChecker
from .core.images import build as image_build, save_image


@click.command
@click.argument('cmd', type=str, default='check')
def cli(cmd):
    checker = HashChecker(current_repo)  # 把当前仓库传进去进行hash值检查
    checker.check_hash()  # 检查其中子模块的hash值是否符合
    if cmd == 'check':
        show_hash(current_repo)  # 展示子模块hash值
    elif cmd == 'build':
        image_build()
    elif cmd == 'save':
        save_image()
    elif cmd == 'gen':
        CONFIG.gen()
    elif cmd == 'show':
        logger.info(CONFIG.repo_list)


if __name__ == '__main__':
    cli()
