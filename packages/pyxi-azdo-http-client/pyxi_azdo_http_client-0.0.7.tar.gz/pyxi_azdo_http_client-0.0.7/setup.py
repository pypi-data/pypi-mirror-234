from setuptools import setup, find_packages

# metadata...
name = "pyxi_azdo_http_client"
description = "A simple HTTP client for interacting with the AzureDevOps API."
author = "Simon Stipcich"
author_email = "stipcich.simon@gmail.com"
url = "https://github.com/stiproot/py-azdo-http-client"
license = "MIT"
keywords = ["python", "package", "azuredevops", "beta"]
version = "0.0.7"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# dependencies...
install_requires = [
    "environs",
]

# setup...
setup(
    name=name,
    version=version,
    packages=find_packages(where="src"),
    package_dir={"pyxi_azdo_http_client": "src/pyxi_azdo_http_client"},
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    keywords=keywords,
    install_requires=install_requires,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
)
