from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="txt2imggen",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Soumalya Das",
    author_email="geniussantu1983@gmail.com",
    description="A module for generating images from text",
    long_description=long_description,
    long_description_content_type="text/markdown",
)