from setuptools import setup, find_packages

setup(
    name="genera",
    version="0.1.10",
    packages=find_packages(),
    python_requires=">=3.10",
    include_package_data=True,
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.10.0",
        "pandas>=2.1.0",
        "biopython>=1.80",
        "primer3-py>=2.0.0",
        "openpyxl>=3.1.0",
    ],
)
