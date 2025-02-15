# -*- coding: utf-8 -*-
import setuptools


with open('readme.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name='yoficator',
    version='0.1.1',
    description='A Russian text yoficator (ёфикатор)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='License :: OSI Approved :: MIT License',
    packages=['yoficator'],
    package_data={
        'yoficator': ['_data/yoficator.dic'],
    },
    install_requires=['regex==2015.11.09'],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=2.7, <3',
)
