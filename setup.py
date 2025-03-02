import setuptools
import os
import bz2

with open('readme.md') as fh:
    long_description = fh.read()


def create_zip():
    with open('lib/md/language/yofication/_data/dictionary.ru_RU.txt', 'rb') as source:
        with bz2.BZ2File('lib/md/language/yofication/_data/dictionary.ru_RU.txt.bz2', 'w') as stream:
            stream.write(source.read())


try:
    create_zip()
    setuptools.setup(
        name='md.language.yofication',
        version='0.1.1',
        description='A Russian text yoficator (ёфикатор)',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license='License :: OSI Approved :: MIT License',
        package_dir={'': 'lib/'},
        packages=['md.language.yofication'],
        package_data={
            'md.language.yofication': ['_data/dictionary.ru_RU.txt.bz2'],
        },
        include_package_data=True,
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
        python_requires='>=3.6',
    )
finally:
    try:
        os.remove('lib/md/language/yofication/_data/dictionary.ru_RU.txt.bz2')
    except FileNotFoundError:
        pass
