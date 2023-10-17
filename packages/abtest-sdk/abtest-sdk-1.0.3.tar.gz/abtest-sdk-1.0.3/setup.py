from setuptools import setup, find_packages

setup(
    name='abtest-sdk',
    version='1.0.3',  # 版本号
    description='ab SDK for phoenix',  # 描述
    author='',
    author_email='',
    url='https://github.com/phoenix-rec/abtest-sdk-python',  # 项目 URL
    packages=find_packages(),  # 自动发现和包含所有包
    install_requires=[  # 依赖列表
        'requests',
        'setuptools'
        # 添加其他依赖
    ],
)