from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="timexwiz",
    version="1.0.1",
    author="UncleDrema",
    author_email="missl.wipiece@gmail.com",
    description="Timexwiz is a simple Python library for time measure, benchmarking and algorithm comparisons.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["measure", "benchmark", "time", "library", "Python"],
    url="https://github.com/UncleDrema/timexwiz",
    packages=["timexwiz"],
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)