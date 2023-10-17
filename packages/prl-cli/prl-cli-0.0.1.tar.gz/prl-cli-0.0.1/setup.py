from setuptools import setup, find_packages

setup(
    name="prl-cli",
    version="0.0.1",
    author="Langston Nashold, Rayan Krishnan",
    packages=find_packages(),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["Click", "gql", "attrs"],
    url="http://pypi.python.org/pypi/prl-cli/",
    description="A CLI tool for creating, managing and running test suites on PlaygroundRL.",
    entry_points={
        "console_scripts": [
            "prl = prl.main:cli",
        ],
    },
)
