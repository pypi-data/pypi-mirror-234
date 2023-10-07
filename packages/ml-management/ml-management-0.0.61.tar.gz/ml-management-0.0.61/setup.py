"""Setup for ml-management package."""
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("VERSION", "r", encoding="utf-8") as f:
    version = f.read()

setup(
    name="ml-management",
    version=version,
    description="Python implementation of model pattern, dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ISPRAS MODIS",
    author_email="modis@ispras.ru",
    maintainer="Maxim Ryndin",
    packages=find_packages(include=["ML_management", "ML_management.*"]),
    include_package_data=True,
    install_requires=[
        "sgqlc==16.1",
        "mlflow==2.4.0",
        "boto3==1.28.15",
        "jsonschema==4.18.4",
        "requests_toolbelt>=0.9.1,<=1",
        "tqdm==4.65.0",
    ],
    data_files=[("", ["VERSION"])],
    python_requires=">=3.8",
)
