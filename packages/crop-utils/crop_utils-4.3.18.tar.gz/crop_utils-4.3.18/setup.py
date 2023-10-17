# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @author :libo

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crop_utils",  # 包名称
    version="4.3.18",  # 版本号
    author="libo",
    author_email="6878595@qq.com",
    description="扩边裁剪，上下裁剪点一致，无法裁剪",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://git.chaomy.com/libo/ecpro-utils.git",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)