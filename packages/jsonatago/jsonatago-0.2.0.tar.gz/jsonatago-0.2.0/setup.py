from setuptools import setup, find_packages

setup(
    name="jsonatago",
    version="0.2.0",
    packages=find_packages(),
    package_data={
        "jsonatago": ["golang/jsonatago.dll"],  # or jsonatago.so for Linux
    },
    install_requires=[
        # Your dependencies here
    ],
)
