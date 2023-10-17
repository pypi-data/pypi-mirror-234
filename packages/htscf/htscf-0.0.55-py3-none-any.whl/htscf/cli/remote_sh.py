from argparse import ArgumentParser

import uvicorn


class CLICommand:
    """通过api远程执行脚本及命令，文档地址: /docs
    """

    @staticmethod
    def add_argments(parser: ArgumentParser):
        add = parser.add_argument
        add("port", help="remote shell外网端口号")

    @staticmethod
    def run(args, parser):
        uvicorn.run("htscf.utils.remote_sh:app", port=int(args.port), host="0.0.0.0")


