from __future__ import print_function
from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name="structured_log_json",
    version="1.0.0-2023",
    author="Qiao.putty&&yangdunstc",  #作者名字
    author_email="yangdunstc@163.com",
    description="Python structured event expression in json log.",
    license="LICENSE",
    url="https://gitee.com/putty_git/structured_event_expression_in_-json_python.git",  #github地址或其他地址
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: System :: Logging',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    python_requires = '>=3.6.9',
    platforms = 'any',
    install_requires=[
             #所需要包的版本号
    ],
    zip_safe=True,
)
