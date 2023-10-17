from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mask2bbox",
    version="0.0.12",
    description="Gets the bounding boxes from a mask file.",
    url="https://github.com/SchapiroLabor/mask2bbox",
    author="Miguel Ibarra",
    author_email="c180l058j@mozmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        "numpy",
        "scikit-image",
        "matplotlib",
    ],
    extras_require={
        "dev": ["pytest>=3.7"],
    },
)

