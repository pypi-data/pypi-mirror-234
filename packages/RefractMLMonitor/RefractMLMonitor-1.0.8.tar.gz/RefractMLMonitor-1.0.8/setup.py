from setuptools import setup, find_packages

with open("drift/requirements.txt") as f:
    requirements =  f.read().splitlines()


setup(
    name = "RefractMLMonitor",
    version = "1.0.8",
    packages = find_packages(),
    install_requires = requirements,
    include_package_data=True
)