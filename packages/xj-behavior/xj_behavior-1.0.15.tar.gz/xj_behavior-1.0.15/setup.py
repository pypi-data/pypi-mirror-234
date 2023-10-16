from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf8') as fp:
    log_desc = fp.read()

setup(
    name='xj_behavior',  # 模块名称
    version='1.0.15',  # 模块版本
    description='行为模块',  # 项目 摘要描述
    long_description=log_desc,  # 项目描述
    long_description_content_type="text/markdown",  # md文件，markdown格式
    packages=find_packages(),  # 系统自动从当前目录开始找包
    license="apache 3.0",
    install_requires=[]
)
