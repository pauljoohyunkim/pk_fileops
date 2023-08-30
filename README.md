# pk_fileops
A soon-to-be collection of programs for specific file management.

Currently available programs are:
* dupe_check: Detect duplicate files on directories.
* sim_image: Similar to dupe_check, but detects similar images.

## Installation
### pip
To install the package through pip,
while at the root directory of the repo,
```
pip install .
```
### No-installation
To try the programs without installation,
you can use
```
python -m [module name]
```
For example, if you want to use *dupe_check*,
```
# Note that dupe_check.py is inside dupe_check directory.
python -m dupe_check.dupe_check
```