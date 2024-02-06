from setuptools import setup, find_packages

setup(
    name="openmindlab",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "fitz", "PyMuPDF"
    ],
)
