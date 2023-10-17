from argparse import ArgumentParser

import uvicorn


class CLICommand:
    """通过PBS task ID查询当前任务执行路径
    """

    @staticmethod
    def add_argments(parser: ArgumentParser):
        add = parser.add_argument
        add("port", help="remote shell外网端口号")

    @staticmethod
    def run(args, parser):
        uvicorn.run("htscf.utils.remote_sh:app", port=args.port, host="0.0.0.0")


