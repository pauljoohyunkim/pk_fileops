from setuptools import setup, find_packages

setup(
    name='pk_fileops',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        line.strip() for line in open('requirements.txt')
    ],
    entry_points={
        'console_scripts': [
            'dupe_check = dupe_check.dupe_check:main',
        ],
    },
)