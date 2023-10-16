from setuptools import setup, find_packages

setup(
    name="puyuan_modelhub",
    version="1.0.0",
    description="A library for managing LLM models",
    author="HSPK",
    author_email="whxway@gmail.com",
    packages=find_packages(exclude=["modelhub.server", "modelhub.server.models"]),
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
