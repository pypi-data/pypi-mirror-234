from setuptools import find_packages, setup

from server_api import __version__

setup(
    name="kubanemil_server_api",
    version=__version__,
    url="https://git-codecommit.eu-central-1.amazonaws.com/v1/repos/server-api",
    author="Kuban Emil",
    author_email="emil3toktobekov@gmail.com",
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=["requests==2.31.0", "sqlmodel==0.0.8", "pydantic>=1.10.12,<2"],
)
