from setuptools import setup
import os

def get_folders(path :str = "resumer"):
    return [
        f"resumer.{f}" for f in os.listdir(path) 
        if os.path.isdir(os.path.join(path, f)) and not f.startswith("_")
    ] + ["resumer"]


setup(
    name='resumer',
    version='1.0.2',
    packages=get_folders(),
    description="pandoc based generator with advanced filter support",
    author="Zackary W",
    license="MIT",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zackaryw/resumer",
    install_requires=[
        "pydantic",
        "click",
        "requests",
    ],
    package_data={
        '' : ["*.tex"]
    },
    entry_points={
        'console_scripts': [
            'resumer = resumer.cli:cli',
        ]
    },
    classifiers=[
        # > 3.11
        "Programming Language :: Python :: 3.11",
    ]
)