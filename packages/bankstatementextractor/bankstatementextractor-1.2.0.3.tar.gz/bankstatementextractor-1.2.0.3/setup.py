from setuptools import setup, find_packages

with open("/Users/anjalimallissery/Downloads/Anjali_BS_Extract/requirements.txt") as f:
    required = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bankstatementextractor",
    version="1.2.0.3",
    author="Anjali",
    author_email="anjalimenon217@gmail.com",
    description=("This repository contains a Python program designed to extract Optical Character Recognition (OCR)"
                 " data from bank statements, detect income and classify expenses"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=required,
    include_package_data=True,
)
