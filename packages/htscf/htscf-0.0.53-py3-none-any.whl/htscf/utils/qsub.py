import sys
from datetime import datetime as __dt
from pathlib import Path
from subprocess import Popen, PIPE
from os.path import exists
import platform


def qsub(nodes=1, cores=28, python_script=sys.argv[0]):
    """
    用于python脚本提交
    :param python_script: 本脚本执行路径
    :param nodes:所用节点数，default:1
    :param cores:每个节点所用核数,default:28
    """
    QSUB_PATH = "qsub.sh"
    if platform.system() == 'Windows':
        return
    if not python_script:
        raise Exception("Please specify python script name!")
    if not exists("run"):
        qsub_data_lines = """
#!/bin/bash
#!/bin/env bash
#PBS -N zh
#PBS -l nodes=1:ppn=28
#PBS -q batch
#PBS -V
cd "${PBS_O_WORKDIR}" || exit
run() {
  local arg
  while getopts "p:" arg
  do
    case $arg in
      p)python "$OPTARG";;
      ?)echo "No such command!";;
    esac
  done
}
run -p "$path"
        """.strip().split("\n")
        for line in qsub_data_lines:
            if line.startswith("#PBS -l"):
                index = qsub_data_lines.index(line)
                qsub_data_lines[index] = f"#PBS -l nodes={nodes}:ppn={cores}"
        with open(QSUB_PATH, "w+") as sh:
            for line in qsub_data_lines:
                sh.write(line + "\n")
        popen = Popen(f'qsub -v path="{python_script}" {QSUB_PATH}', shell=True, stdout=PIPE, stderr=PIPE)
        popen.wait()
        if platform.system() == 'Windows':
            info = popen.stdout.read().decode("gbk")
            error = popen.stderr.read().decode("gbk")
        else:
            info = popen.stdout.read().decode("utf-8")
            error = popen.stderr.read().decode("utf-8")
        print("任务ID：", info, end="")
        Path("run").write_text(info)
        Path("run").write_text(error)
        exit()
    else:
        with open("run", "a+") as f1:
            f1.write(f"start running! {__dt.now()}")


if __name__ == '__main__':
    qsub(1, 20, "test.py")
