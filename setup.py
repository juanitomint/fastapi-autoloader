from setuptools import find_packages, setup

setup(
    name="fastapi-autoloader",
    version="0.1.0",
    description="A Python package for dynamic routing in FastAPI.",
    author="",
    packages=find_packages(),
    install_requires=[
        "fastapi",
    ],
    python_requires=">=3.7",
)
