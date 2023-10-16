from pathlib import Path
from setuptools import setup, find_packages


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="fkriza-calculator",
    version="1.0.1",
    author="Filip Křížan",
    packages=find_packages(),
    py_modules=["fkrizan-calculator"],
    install_requires=[],
    description="""
                This Module implements a simple calculator interface with in instance memory,
                supporting basic arithmetical operations.
                """,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
