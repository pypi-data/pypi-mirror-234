"""vxsched 主函数"""
import argparse

from pathlib import Path
from typing import Union
from vxutils.sched.core import vxsched
from vxutils import logger


def init(work_path: Union[str, Path] = "./") -> None:
    if not isinstance(work_path, Path):
        work_path = Path(work_path)

    for sub_dir in ["log", "etc", "mod"]:
        work_path.joinpath(sub_dir).mkdir(parents=True, exist_ok=True)
        logger.info("创建文件目录 %s", work_path.joinpath(sub_dir).absolute())


def main(args=None) -> None:
    if args is None:
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--script", help="启动组件", default="scheduler")

        parser.add_argument(
            "-c",
            "--config",
            help="config json file path: etc/config.json",
            default="config.json",
            type=str,
        )
        parser.add_argument(
            "-m",
            "--mod",
            help="module directory path : mod/ ",
            default="mod/",
            type=str,
        )
        parser.add_argument(
            "-v", "--verbose", help="debug 模式", action="store_true", default=False
        )
        parser.add_argument(
            "-i", "--init", help="初始化文件目录树", action="store_true", default=False
        )
        args = parser.parse_args()

    if args.init:
        init()
        return

    if args.verbose:
        logger.setLevel("DEBUG")

    vxsched.server_forerver(args.config, args.mod)


if __name__ == "__main__":
    main()
