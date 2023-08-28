from setuptools import setup, find_packages

setup(
    name='pk_fileops',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List any dependencies your script needs
    ],
    entry_points={
        'console_scripts': [
            'dupe_check = dupe_check.dupe_check:main',
        ],
    },
)