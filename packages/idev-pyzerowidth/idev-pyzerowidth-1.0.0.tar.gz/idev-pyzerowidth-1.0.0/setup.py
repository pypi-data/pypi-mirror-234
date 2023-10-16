import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "idev-pyzerowidth",
    version = "1.0.2",
    author = "IrtsaDevelopment",
    author_email = "irtsa.development@gmail.com",
    description = "A simple set of functions in python for encoding messages into zero-width characters.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/IrtsaDevelopment/PyZeroWidth",
    project_urls = {
        "Bug Tracker": "https://github.com/IrtsaDevelopment/PyZeroWidth/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "idev-pyzerowidth"},
    packages=["PyZeroWidth"],
    python_requires = ">=3.6"
)