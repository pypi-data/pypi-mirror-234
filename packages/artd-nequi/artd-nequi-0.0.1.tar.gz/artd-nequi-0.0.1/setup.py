from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name="artd-nequi",
    version="0.0.1",
    include_package_data=True,
    author="Jonathan Urzola Maladonado",
    author_email="jonathan@artd.com.co",
    description="A Django app to integrato with Nequi payment gateway",
    long_description_content_type="text/markdown",
    url="https://www.artd.com.co/",
    long_description=long_description,
    packages=find_packages(),
    keywords=["pypi", "cicd", "python"],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
