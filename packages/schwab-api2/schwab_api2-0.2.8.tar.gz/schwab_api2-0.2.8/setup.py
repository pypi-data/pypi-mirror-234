from distutils.core import setup
import os.path
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="schwab_api2",
    packages=setuptools.find_packages(),
    version="0.2.8",
    license="MIT",
    description="Unofficial Schwab API wrapper in Python 3.",
    author="MaxxRK",
    author_email="maxxrk@pm.me",
    url="https://github.com/MaxxRK/schwab-api2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/MaxxRK/schwab-api2/releases/tag/V_028",
    keywords=["schwab", "python3", "api", "unofficial", "schwab-api", "schwab charles api"],
    install_requires=["playwright",
                      "playwright-stealth",
                      "pyotp",
                      "python-vipaccess",
                      "beautifulsoup4"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        
    ],
)