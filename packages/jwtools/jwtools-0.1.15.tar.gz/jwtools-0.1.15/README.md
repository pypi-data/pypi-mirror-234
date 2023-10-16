# jwtools
集微工具箱，包括各种常用操作，后续不断完善

### 构建
在项目文件夹中运行以下命令
```shell
python setup.py sdist bdist_wheel
```

### 上传：
```shell
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
或
python -m twine upload dist/*
```
按照提示，输入pypi的用户名、密码，就可以成功了。若中途提示有些库没有安装，则使用pip安装一下，需要用到twine库。

### 使用

#### 安装或更新
pip3 install jwtools
pip3 install --upgrade jwtools

#### 代码使用
```python
from jwtools.func import *
from jwtools.io_util import *

mm5 = get_text_md5("dddd")
print(mm5)

# write_text_to_file
result = write_text_to_file("D:/test/test123.txt", mm5)
print(result)

# read_text_from_file
cc = read_text_from_file("D:/test/test123.txt")
print(cc)
```