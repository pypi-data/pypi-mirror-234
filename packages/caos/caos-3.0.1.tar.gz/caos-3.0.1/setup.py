from textwrap import dedent
from setuptools import find_packages, setup
from caos import __VERSION__
from caos._internal.console import CAOS_CONSOLE_LOGO

with open(file="README.md", mode="r") as file:
    full_description = file.read()


setup(
    name="caos",
    version=__VERSION__,
    author="Camilo Ospina",
    author_email="camilo.ospinaa@gmail.com",
    description="A simple dependency management tool and tasks executor for Python projects",
    long_description=full_description,
    long_description_content_type='text/markdown',
    url="https://github.com/caotic-co/caos/",
    keywords='caos virtualenv dependencies manager poetry pip-tools npm pnpm bun maven composer pipenv venv easy_install '
             'setuptools wheel',
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    platforms = ["Windows", "Linux", "Mac OS-X", "Unix"],

    packages=find_packages(exclude=["tests", "tests.*"]),

    package_data={
        "": ["*.*", "README", "LICENSE"],
    },

    entry_points={
        "console_scripts": ["caos=caos._cli:cli_entry_point"],
    },

    install_requires=[
        'pip>=9.0.0',
        'virtualenv>=16.0.0',
    ],

    python_requires=">=3.6",

)

print(dedent(CAOS_CONSOLE_LOGO)[1:] + (" " * 28) + "v{}".format(__VERSION__))

