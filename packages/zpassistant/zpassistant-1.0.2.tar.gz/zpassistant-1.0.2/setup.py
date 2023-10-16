import setuptools #导入setuptools打包工具
import os
import shutil
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("version.txt", "r", encoding="utf-8") as fh:
    version = fh.read()
    # 版本用.分割,反向遍历,如果不是数字的忽略,是数字的加一
    print(version)
    version_list = version.split('.')
    for i in range(len(version_list)-1,-1, -1):
        if version_list[i].isdigit():
            version_list[i] = str(int(version_list[i])+1)
            break
    # 写入version.txt中
    version = '.'.join(version_list)
    print("package version is : " + version)
with open("version.txt", "w", encoding="utf-8") as fh:
    fh.write(version)

# 删除build,dist文件夹
if os.path.exists("build"):
    shutil.rmtree("build")
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("zpassistant.egg-info"):
    shutil.rmtree("zpassistant.egg-info")

setuptools.setup(
    name="zpassistant", # 用自己的名替换其中的YOUR_USERNAME_
    version=version,    #包版本号，便于维护版本
    author="zhitao.mao",    #作者，可以写自己的姓名
    author_email="mzt12450@163.com",    #作者联系方式，可写自己的邮箱地址
    description="公司内部使用单点登录",#包的简述
    long_description=long_description,    #包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://gitee.com/naozeizei",    #自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',    #对python的最低版本要求
    install_requires=[
        "selenium"
    ]
)