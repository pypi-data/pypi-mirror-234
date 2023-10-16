# TD SDK Core Python

基于 Python3 核心框架，集成 flask，nacos，zip

## 更新依赖

```
pipreqs ./ --encoding utf-8  --force
```

## 安装依赖

```
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/  --trusted-host  mirrors.aliyun.com
```

## 制作包

```
# 构建
python setup.py build

# 直接源码安装
python setup.py install

# 打包dist, zip或tar.gz
python setup.py sdist

# 打包whl
python setup.py bdist_wheel
```

## 上传到 PyPi

```
python3 -m twine upload dist/*

# windows下使用以下命令上传
twine upload dist/*
```

## 上传包

`https://packages.simmed.cn/#browse/upload:pypi`

## 安装包

```
pip install simmed

# 环境依赖,注意python版本
yum install python3-devel -y

# 加速
pip install xxxx -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 引用包

```
import simmed.config as config
from simmed.simmed_core import init_flask_app, set_zipkin_tags, get_config, rpc_rest_service, log
```
