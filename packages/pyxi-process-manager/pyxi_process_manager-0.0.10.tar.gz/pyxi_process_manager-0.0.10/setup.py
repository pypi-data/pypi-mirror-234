from setuptools import setup, find_packages

# metadata...
name = "pyxi_process_manager"
description = "A simple process manager in python."
author = "Simon Stipcich"
author_email = "stipcich.simon@gmail.com"
url = "https://github.com/stiproot/py-process-manager"
license = "MIT"
keywords = ["python", "package", "process", "beta"]
version = "0.0.10"

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
    package_dir={"pyxi_process_manager": "src/pyxi_process_manager"},
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
