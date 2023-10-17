from setuptools import setup, find_packages

setup(
    author="Paul de Fusco",
    description="A Python Package for interacting with Cloudera Data Engineering Clusters",
    long_description="A Python Package for interacting with Cloudera Data Engineering Clusters",
    name="cdepy",
    version="0.1.1",
    packages=find_packages(include=["cdepy", "cdepy.*"]),
    install_requires=["pyparsing==3.0.9", "requests-toolbelt==1.0.0", "xmltodict==0.13.0"],
    python_requires=">=2.7",
    readme="README.md"
)
