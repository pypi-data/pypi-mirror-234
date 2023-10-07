from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="webio_api",
    version="0.1.10",
    author="nasWebio",
    author_email="devel_team@chomtech.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nasWebio/webio_api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
