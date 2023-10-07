

import os
import sys
from setuptools import setup, find_packages
basedir = os.path.dirname(os.path.abspath(__file__))

long_description = None
with open(os.path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='autorunx',
    version='1.0.1',
    author='Xuanfq',
    author_email='2624208682@qq.com',
    license='MIT',
    url='https://github.com/Xuanfq/AutoRunX-Python',
    description='AutoRunX is an open source low code framework.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["lib.{}".format(sub)
              for sub in find_packages(where='lib', include=['*'])],
    py_modules=['autorunx', 'globals'],
    entry_points={
        'console_scripts': [
            'autorunx = autorunx:main',
            'arx = autorunx:main'
        ]
    },
    classifiers=[  # https://pypi.org/pypi?%3Aaction=list_classifiers
        # 发展时期,常见的如下
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # 开发的目标用户
        'Intended Audience :: Developers',
        # 属于什么类型
        'Topic :: Software Development :: Build Tools',
        # 许可证信息
        'License :: OSI Approved :: MIT License',
        # 目标 Python 版本
        'Programming Language :: Python :: 3.9',
    ],
    keywords=['autorun','auto','run','automatic'],
)
