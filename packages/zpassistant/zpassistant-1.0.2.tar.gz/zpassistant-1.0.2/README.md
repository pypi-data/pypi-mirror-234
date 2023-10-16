# 工具包
## 单点登录工具包

``` shell
# 安装打包工具
python3 -m pip install --user --upgrade twine
# 打包指令
python3 setup.py sdist bdist_wheel
# 上传
python3 -m twine upload dist/*
# 更新zpassistant
pip3 install -i https://pypi.org/simple --upgrade zpassistant 