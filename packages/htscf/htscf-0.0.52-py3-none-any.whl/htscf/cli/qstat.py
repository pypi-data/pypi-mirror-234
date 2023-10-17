from argparse import ArgumentParser
from pathlib import Path
from subprocess import Popen, PIPE
from sys import argv


class CLICommand:
    """通过PBS task ID查询当前任务执行路径
    """

    @staticmethod
    def add_argments(parser: ArgumentParser):
        add = parser.add_argument
        add("taskId", help="pbs任务名")

    @staticmethod
    def run(args, parser):
        getPath(args.taskId)


def getPath(taskId):
    popen = Popen(f"qstat -f {taskId}", stdout=PIPE, shell=True)
    popen.wait()
    lines = popen.stdout.read().decode("utf-8").split("\n")[1:]
    arr = []
    while lines:
        line = lines.pop(0)
        if line.startswith("\t") or line.endswith(",") or line.startswith("}"):
            line = line.strip()
            arr[-1] += line
        else:
            line = line.strip()
            if line:
                arr.append(line)
    config = {}
    for i in arr:
        key, value = i.split("=", maxsplit=1)
        key = key.strip()
        value = value.strip()
        config[key] = value
    outputPath = config["Output_Path"].split(":", maxsplit=1)[1]
    rootPath = Path(outputPath).parent
    print(rootPath)
