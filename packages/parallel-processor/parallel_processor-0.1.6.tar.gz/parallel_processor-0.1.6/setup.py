# encoding:utf8

from setuptools import setup

with open("README.md", "r") as fin:
    long_description = fin.read()

setup(name='parallel_processor',
      version='0.1.6',
      description='Parallelling Data Processor',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/Fakekid/parallel-processor',
      author='Xiaolei Lian,Yue Wang,TingTing Gong,Hang Deng',
      author_email='lian19931201@gmail.com,wangyue29@tal.com,gongtingting@safeis.cn,denghang@safeis.cn',
      license='MIT',
      include_package_data=False,
      packages=['parallel_processor'],
      python_requires='>=3.6',
      install_requires=[  # 依赖列表
          'numpy>=1.14.3',
      ],
      zip_safe=False)
