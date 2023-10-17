from argparse import ArgumentParser
from htscf.io.vaspIO import writeIncar
from os import system


class CLICommand:
    """bandDecomposedCharge
    """

    @staticmethod
    def add_argments(parser: ArgumentParser):
        pass

    @staticmethod
    def run(args, parser):
        bandDecomposedCharge()


def bandDecomposedCharge():
    iband = []
    kpuse = []
    cmd0 = input("请输入vasp路径：")  # 默认计算所有K点
    cmd1 = input("请指定特定k点（默认计算所有k点）：")  # 默认计算所有K点
    cmd2 = input("请指定计算的能带序号:")  # 指定计算的能带序号
    cmd3 = input("Mix Kpoints?")  # 默认叠加所有k点
    cmd4 = input("Mix bands?")  # 默认合并所有选定能带
    lsepb = False
    lsepk = False
    if cmd3:
        lsepb = True
    if cmd4:
        lsepk = True
    kpuse.extend(cmd1.split(" "))
    iband.extend(cmd2.split(" "))
    data = {"directory": "./INCAR",
            "istart": 1,
            "lpard": True,
            "lsepb": lsepb,
            "lsepk": lsepk}
    if kpuse[0]:
        data["kpuse"] = list(map(lambda x: int(x), kpuse))
    if iband[0]:
        data["iband"] = list(map(lambda x: int(x), iband))
    writeIncar(".", **data)
    system(cmd0)
