from setuptools import setup
packages = ['zlgsendcan']# 唯一的包名，自己取名
setup(
    name='zlgsendcan',
    version='1.2.6',
    author='liuzhong',
    author_email='liuzhong@auto-link.com.cn',
    description='zlg send canmsg',
    packages=packages,
    include_package_data=True,
    package_data={'zlgsendcan': ['kerneldlls/*','*.dll']},
    install_requires=[
        'cantools',
        'PyYAML',
        'airtest-sd'
    ],
)