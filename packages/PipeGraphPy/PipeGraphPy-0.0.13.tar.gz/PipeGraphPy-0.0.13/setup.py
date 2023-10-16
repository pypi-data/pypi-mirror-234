# coding:utf-8

from setuptools import setup

def get_requirements():
    with open("requirements.txt") as requirements:
        des_pkg = [
            line.split("#", 1)[0].strip()
            for line in requirements
            if line and not line.startswith(("#", "--"))
        ]

        return des_pkg


setup(
    name="PipeGraphPy",  # 应用名
    description="核心算法框架",
    license="Private",
    include_package_data=True,
    install_requires=get_requirements(),
)
