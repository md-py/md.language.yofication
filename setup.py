import setuptools
import os
import bz2


with open('readme.md') as fh:
    long_description = fh.read()


def create_zip():
    with open('yoficator/_data/dictionary.ru_RU.txt', 'rb') as source:
        with bz2.BZ2File('yoficator/_data/dictionary.ru_RU.txt.bz2', 'w') as stream:
            stream.write(source.read())


try:
    create_zip()
    setuptools.setup(
        name='yoficator',
        version='0.1.7',
        description='A Russian text yoficator (ёфикатор)',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license='License :: OSI Approved :: MIT License',
        packages=['yoficator'],
        package_data={
            'yoficator': ['_data/dictionary.ru_RU.txt.bz2'],
        },
        include_package_data=True,
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
        python_requires='>=3',
    )
finally:
    try:
        os.remove('yoficator/_data/dictionary.ru_RU.txt.bz2')
    except FileNotFoundError:
        pass
