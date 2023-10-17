# 高通量计算流程

## 创建流程步骤

```python
from htscf.core.createStep import create

create(
    _id="xxxx",  # 步骤id
    program="python",  # 执行的程序名 
    script="...........",  # 执行的脚本内容
    settings={"a": "12"},  # 执行脚本相关设置
    dbName="htscf",  # 数据库名
    collectionName="xxx",  # 集合名
    host="192.1.1.100",  # 数据库Ip
    port=27017  # 数据库端口
)
```

## 脚本格式

```python
from sys import argv

rootPath, settingsId, prevLogId = argv[1:]

# 输出到下一步的数组使用print,即可传递到下一步的prevData
print(rootPath, settingsId)
```

## 流程化运行

```python
from htscf.core.flow import workflow

workflow(
    "./xxx",  # 流程执行根目录
    stepIds=["xx", "yy"],  # 按照该数组中排列一次执行每一步
    dbName="test",  # 数据库名
    stepsCollectionName="steps",  # 流程数组集合
    stepLogCollectionName="log",  # 
    host="42.244.24.75",
    port=27000
)

```