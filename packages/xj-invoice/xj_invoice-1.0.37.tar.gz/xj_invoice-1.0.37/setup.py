# encoding: utf-8
"""
@project: djangoModel->setup
@author: 高栋天
@Email: 1499593644@qq.com
@synopsis: 模块打包文件
@created_time: 2022/6/18 15:14
"""
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf8') as fp:
    log_desc = fp.read()

setup(
    name='xj_invoice',  # 模块名称
    version='1.0.37',  # 模块版本
    description='发票模块',  # 项目 摘要描述
    long_description=log_desc,  # 项目描述
    long_description_content_type="text/markdown",  # md文件，markdown格式
    author='高栋天',  # 作者
    author_email='1499593644@qq.com',  # 作者邮箱
    maintainer=["高栋天"],  # 维护者
    maintainer_email="angelvy@foxmail.com",  # 维护者的邮箱地址
    packages=find_packages(),  # 系统自动从当前目录开始找包
    license="apache 3.0",
    install_requires=[]
)
