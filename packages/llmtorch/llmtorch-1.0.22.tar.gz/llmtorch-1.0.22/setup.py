# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 22:06:42 2022

@author: xx_zheng
"""

from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r",encoding='utf-8') as f:
    long_description = f.read()

setup(name='llmtorch',  # 包名
      version='1.0.22',  # 版本号
      description='llm model process for pytorch',
      long_description=long_description,
      author='llmtorch team',
      author_email='1027763372@qq.com',
      url='',
      license='BSD License',
      install_requires=['torch>=1.9.0','torchtext','tiktoken','tqdm'],
      # 'torch==2.0.0',  # 另一个示例依赖项
      packages=find_packages(),
      platforms=["all"],
      long_description_content_type="text/markdown",
      include_package_data=True,
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      keywords="machine-learning, deep-learning, ML, DL, pytorch, torch, llm",
      )