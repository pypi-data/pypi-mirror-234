from setuptools import setup, find_packages


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()


setup(
    name="UdemyCalculator_aag",
    version="1.0.0",
    packages=find_packages(),
    install_require=[],
    url="",
    LICENCE="MIT",
    author="Alessandro Guarita",
    description="This is my udemy calculator package",
    python_requires=">=3.6",
)
