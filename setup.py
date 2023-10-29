from setuptools import setup, find_packages  # type: ignore


REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

# get version from module stadsarkiv_client
VERSION = ""
with open("gpt_translator/__init__.py", "r") as fh:
    for line in fh.readlines():
        if line.startswith("__version__"):
            VERSION = line.split("=")[1].strip().replace('"', "")
            break

setup(
    name="gpt-translator",
    version=VERSION,
    description="Translate documents using GPT",
    url="https://github.com/diversen/gpt-translator",
    author="Dennis Iversen",
    author_email="dennis.iversen@gmail.com",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    # package_data={"stadsarkiv_client": ["templates/**/**", "templates/**", "static/**/**", ".env-dist"]},
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "gpt-translator = gpt_translator.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.10",
    ],
)