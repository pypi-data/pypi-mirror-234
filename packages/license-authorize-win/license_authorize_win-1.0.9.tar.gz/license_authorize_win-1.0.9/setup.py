#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
# @Time    :  2023/5/19 14:35
# @Author  : chenxw
# @Email   : gisfanmachel@gmail.com
# @File    : setup.py
# @Descr   : 
# @Software: PyCharm


# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(

    # name="license_authorize",  # Required 项目名称
    name="license_authorize_win",  # Required 项目名称
    version="1.0.9",  # Required 发布版本号
    description="A tools for license authorize in windows",  # Optional 项目简单描述
    long_description=long_description,  # Optional 详细描述
    long_description_content_type="text/markdown",  # 内容类型
    url="https://github.com/gisfanmachel/licenseAuthorize",  # Optional github项目地址
    author="gisfanmachel",  # Optional 作者
    author_email="gisfanmachel@gmail.com",  # Optional 作者邮箱
    classifiers=[  # Optional 分类器通过对项目进行分类来帮助用户找到项目, 以下除了python版本其他的 不需要改动

        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],

    keywords="license,authorize, setuptools, development",  # Optional 搜索关键字

    # packages=find_packages(),  # Required

    packages=['license_authorize_win'],  # Required
    # 打包要包含的文件
    package_data={
        'license_authorize_win': ["*.pyd"]
    },

    python_requires=">=3.7, <4",  # python 版本要求

    install_requires=["pycryptodome"],  # Optional 第三方依赖库

)