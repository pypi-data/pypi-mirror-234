from setuptools import setup, find_packages
from pathlib import Path

# Get the current directory of the setup.py file (as this is where the README.md will be too)
current_dir = Path(__file__).parent
long_description = (current_dir / "README.md").read_text()

# Set up the package metadata
setup(
    name="psusannx_utils",
    author="Jamie O'Brien",
    description="A package for storing functions that are used across multiple functions & modules in the PSUSANNX project..",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.4",
    packages=find_packages(include=["psusannx_utils", "psusannx_utils.*"]),
    install_requires=[
        "pandas>=1.3.4",
        "beautifulsoup4>=4.12.2"
    ],
    project_urls={
        "Source Code": "https://github.com/jamieob63/psusannx_utils.git",
        "Bug Tracker": "https://github.com/jamieob63/psusannx_utils.git/issues",
    }
)