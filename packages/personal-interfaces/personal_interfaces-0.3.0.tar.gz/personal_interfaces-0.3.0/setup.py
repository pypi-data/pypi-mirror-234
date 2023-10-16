"""
Whole setup for the package.
"""
import re
from setuptools import setup, find_packages


def read_version() -> str:
    """Read the version from the given _version.py file

    Returns:
        - Version string

    Raise:
        - TypeError: If the version could not be find.
    """
    with open("personal_interfaces/_version.py", "r", encoding="utf-8") as version_file:
        version_coincidence = re.search(
            r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    # Now, check for the version coincidence
    if version_coincidence is None:
        raise TypeError("Couldn't find the version in the given file.")
    version = version_coincidence.group(1)
    # Return the version
    return version


def long_description() -> str:
    """Open the `README.md` file and return the long description

    Returns:
        - All the `README.md` as a simple and large string
    """
    with open("./README.md", encoding="utf-8") as file:
        description = file.readlines()
    return "".join(line for line in description)


setup(
    name='personal_interfaces',
    version=read_version(),
    long_description=long_description(),
    long_description_content_type='text/markdown',
    author='Ricardo Leal',
    author_email='ricardo.lealpz@gmail.com',
    maintainer='Ricardo Leal',
    maintainer_email='ricardo.lealpz@gmail.com',
    url="https://github.com/ricardoleal20/personal_interface/",
    packages=find_packages(
        include=['personal_interfaces', 'personal_interfaces.*']),
    include_package_data=True,
    python_requires=">=3.8, <4",
    install_requires=[
        'deta>=1.2.0',
        'uvicorn>=0.23.2',
        'fastapi>=0.103.2',
        'attrs>=23.1.0',
        'rich>=13.6.0',
        'pyjwt>=2.8.0'
    ],
    keywords="development, personal_usage",
    classifiers=[
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    project_urls={  # Optional
        "Bug Reports": "https://github.com/ricardoleal20/personal_interface/issues",
    },
)
