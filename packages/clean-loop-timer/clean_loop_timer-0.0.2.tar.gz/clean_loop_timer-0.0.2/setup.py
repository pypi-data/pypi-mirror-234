from setuptools import setup, find_packages
from pathlib import Path

VERSION = "0.0.2"
DESCRIPTION = "Easy-to-use timer for profiling complex loops in dataset generation and neural network training"
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="clean_loop_timer",
    version=VERSION,
    author="Tyler Lum",
    author_email="tylergwlum@gmail.com",
    url="https://github.com/tylerlum/clean_loop_timer",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["tqdm", "pandas", "tabulate"],
    keywords=["python", "profiling", "timer", "loop"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
