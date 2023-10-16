# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from kuto import __version__, __description__

try:
    long_description = open(os.path.join('kuto', "README.md"), encoding='utf-8').read()
except IOError:
    long_description = ""

setup(
    name="kuto",
    version=__version__,
    description=__description__,
    author="杨康",
    author_email="772840356@qq.com",
    url="https://gitee.com/bluepang2021/kuto",
    platforms="Android,IOS,Web,Api,Mac,Win",
    packages=find_packages(),
    long_description=long_description,
    python_requires='>=3.9',
    classifiers=[
        "Programming Language :: Python :: 3.9"
    ],
    include_package_data=True,
    package_data={
        r'': ['*.yml'],
    },
    install_requires=[
        'requests-toolbelt==0.10.1',
        'jmespath==0.9.5',
        'jsonschema==4.17.0',
        'pytest==6.2.5',
        'pytest-rerunfailures==10.2',
        'pytest-xdist==2.5.0',
        'allure-pytest==2.9.45',
        'click~=8.1.3',
        'loguru==0.7.0',
        'urllib3==1.26.15',
        'PyYAML~=6.0'
    ],
    extras_require={
        "web": ['playwright==1.33.0', 'opencv-python==4.6.0.66'],
        "pc": ['PyAutoGUI==0.9.54', 'opencv-python==4.6.0.66'],
        "app": ['uiautomator2==2.16.23', 'tidevice==0.6.1', 'facebook-wda==1.4.6',
                'opencv-python==4.6.0.66', 'easyocr==1.7.0', 'Pillow==9.5.0', 'filelock==3.12.2'],
        "excel": ['pandas==1.3.4', 'openpyxl==3.0.9', 'XlsxWriter==3.0.2'],
        "encrypt": ["pycryptodome==3.14.1"],
    },

    entry_points={
        'console_scripts': [
            'kuto = kuto.cli:main'
        ]
    }
)
