from setuptools import setup, find_packages  # type: ignore
from gpt_translator import __version__ as version


REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]


setup(
    name="gpt-translator",
    version=version,
    description="Translate documents using GPT",
    url="https://github.com/diversen/gpt-translator",
    author="Dennis Iversen",
    author_email="dennis.iversen@gmail.com",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
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
