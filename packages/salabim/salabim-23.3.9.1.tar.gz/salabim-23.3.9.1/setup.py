from setuptools import setup

with open("readme.md", "r") as f:
    long_description = f.read()

setup(
    name="salabim",
    packages=["salabim"],
    version="23.3.9.1",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="discrete event simulation in Python",
    author="Ruud van der Ham",
    author_email="info@salabim.org",
    url="https://github.com/salabim/salabim",
    download_url="https://github.com/salabim/salabim",
    keywords=["statistics", "math", "simulation", "des", "discrete event simulation"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
)

