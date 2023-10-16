from setuptools import setup, find_packages
from pathlib import Path

VERSION = "0.0.2"
DESCRIPTION = "Function decorator that ensures that no global and no nonlocal variables are used, making Jupyter notebooks much safer"
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="no_global_nonlocal_vars",
    version=VERSION,
    author="Tyler Lum",
    author_email="tylergwlum@gmail.com",
    url="https://github.com/tylerlum/no_global_nonlocal_vars",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "jupyter", "notebook", "decorator", "global", "nonlocal"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
