import pathlib
from setuptools import setup


# The directory containing this file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="tdta",
    version="0.0.20.dev1",
    description="The aim of this project is to provide taxonomy development tools custom actions.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hkir-dev/taxonomy-development-tools-actions",
    author="",
    license="Apache-2.0 license",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    packages=["tdta"],
    include_package_data=True,
    install_requires=['requests'],
    entry_points={
        "console_scripts": [
            "tdta=tdta.__main__:main",
        ]
    },
)
