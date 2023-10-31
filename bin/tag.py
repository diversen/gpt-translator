#!/usr/bin/env python3

"""
This script is used to bump the version of the package.
It will change the version in the pyproject.toml file,
the __init__.py file and the README.md file.

It will exit if there are uncommited changes to prevent
accidental commits.

Usage:

    ./bin/tag.py <version>

"""

import sys
import os

# get first argument as version
try:
    version = sys.argv[1]
except IndexError:
    print("No version provided")
    print("Usage: ./bin/tag.py <version>")
    sys.exit(1)


# # python function that changes the pyproject.toml version
# def change_pyproject_version(version):
#     with open("pyproject.toml", "r") as f:
#         lines = f.readlines()
#     with open("pyproject.toml", "w") as f:
#         for line in lines:
#             if line.startswith("version ="):
#                 f.write(f'version = "{version}"\n')
#             else:
#                 f.write(line)


# python function that changes the __init__.py version
def change_init(version):
    with open("./gpt_translator/__init__.py", "r") as f:
        lines = f.readlines()
    with open("./gpt_translator/__init__.py", "w") as f:
        for line in lines:
            if line.startswith("__version__ ="):
                f.write(f'__version__ = "{version}"\n')
            else:
                f.write(line)


# change in README. Search for this string below <!-- LATEST-VERSION-START -->
# and change the line to \tpip install git+https://github.com/diversen/gpt-translator@{version}
def change_readme(str_search, replace):
    dynamic_next_line = False
    with open("README.md", "r") as f:
        lines = f.readlines()
    with open("README.md", "w") as f:
        for line in lines:
            if dynamic_next_line:
                f.write(replace)
                dynamic_next_line = False
            elif line.startswith(str_search):
                f.write(line)
                dynamic_next_line = True
            else:
                f.write(line)


# check if something needs to be commited
# if something needs to be commited, exit
if os.system("git diff-index --quiet HEAD --") != 0:
    print("There are uncommited changes")
    sys.exit(1)

change_readme("<!-- LATEST-VERSION-PIPX -->", f"\tpipx install git+https://github.com/diversen/gpt-translator@{version}\n")
change_readme("<!-- LATEST-VERSION-PIP -->", f"\tpip install git+https://github.com/diversen/gpt-translator@{version}\n")
# change_pyproject_version(version)
change_init(version)

# commit the changed files
os.system("git add .")
os.system(f'git commit -m "bump version to {version}"')
os.system("git push")

# create tag
os.system(f'git tag -a {version} -m "bump version to {version}"')
os.system("git push --tags")