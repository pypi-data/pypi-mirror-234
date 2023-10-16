from setuptools import find_packages, setup

from server_api import __version__

setup(
    name="server_api",
    version=__version__,
    url="https://git-codecommit.eu-central-1.amazonaws.com/v1/repos/server-api",
    author="Lemon AI",
    author_email="dev@lemon-ai.com",
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=["requests==2.31.0", "sqlmodel==0.0.8", "pydantic>=1.10.12,<2"],
)
