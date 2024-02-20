from setuptools import setup, find_packages

setup(
    name="openmindlab",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "fitz", "PyMuPDF"
    ],
    author='Konstantin Kiselev',
    author_email='kostyakiselev@gmail.com.com',
    description='Пакет для обработки данных экспериментов.',
    keywords='',
)
