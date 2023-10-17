from setuptools import setup, find_packages

import randog


def load_readme() -> str:
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="randog",
    version=randog.__version__,
    project_urls={
        "Bug Tracker": "https://github.com/unaguna/random-obj-generator/issues",
        "Documentation": "https://unaguna.github.io/random-obj-generator/",
        "Source Code": "https://github.com/unaguna/random-obj-generator",
    },
    author="k-izumi",
    author_email="k.izumi.ysk@gmail.com",
    maintainer="k-izumi",
    maintainer_email="k.izumi.ysk@gmail.com",
    description="Generate data randomly",
    long_description=load_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests",)),
    install_requires=[],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Utilities",
    ],
)
