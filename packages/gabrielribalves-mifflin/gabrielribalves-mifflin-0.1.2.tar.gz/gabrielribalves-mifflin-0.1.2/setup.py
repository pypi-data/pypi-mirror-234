from setuptools import setup, find_packages
import os

def myRead(*paths):
    """Read the contents of a text file safely.
    >>> read("dundie", "VERSION ")
    '0.1.0'
    >>> read("README.md")
    ...
    """
    rootPath = os.path.dirname(__file__)
    filePath = os.path.join(rootPath, *paths)
    with open(filePath) as file_:
        return file_.read().strip()
    
def readRequirements(path):
    return [
        line.strip()
        for line in myRead(path).split("\n")
        if not line.startswith(("#","git+",'"',"-"))
    ]

setup(
    name="gabrielribalves-mifflin",
    version="0.1.2",
    description="Reward Point System for Dunder Mifflin",
    long_description=myRead("README.md"),
    long_description_content_type="text/markdown",
    author="Gabriel Goncalves",
    packages=find_packages(exclude=["integration"]),
    include_package_data=True,
    entry_points={
        "console_scripts":["gabrielribalves-mifflin = dundie.__main__:main"]
    },
    install_requires=readRequirements("requirements.txt"),
    extras_require={
        "test": readRequirements("requirements.test.txt"),
        "dev": readRequirements("requirements.dev.txt")
    }
)