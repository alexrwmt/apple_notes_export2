from setuptools import setup, find_packages

setup(
    name="apple-notes-sync",
    version="0.1.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "black",
        "isort",
        "pylint",
    ],
    python_requires=">=3.8",
) 