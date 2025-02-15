import setuptools


with open('readme.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name='yoficator',
    version='0.1.6',
    description='A Russian text yoficator (ёфикатор)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='License :: OSI Approved :: MIT License',
    packages=['yoficator'],
    package_data={
        'yoficator': ['_data/dictionary.ru_RU.txt'],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3',
)
