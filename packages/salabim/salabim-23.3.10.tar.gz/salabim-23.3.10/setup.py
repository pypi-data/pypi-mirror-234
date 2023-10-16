from setuptools import setup

long_description = """salabim
-------
Object oriented discrete event simulation and animation in Python.

Discrete event simulation (DES) can be used in a variety of logistics applications:

* production facilities
* warehousing
* (air)ports
* hospitals
* mining
* materials handling
* steel mills

, but also in other areas, like computer network analysis.

Salabim follows a well proven and very intuitive ame process description method (like Tomas and Must).
The package provides

* components
* queues
* resources
* stores
* states
* monitors for data collection and presentation
* 2D animation (including video production)
* 3D animation (including video production)
* tracing facilities
* advanced statistical sampling

In contrast to some other Python DES packages it is not required to use yield statements for the process control.
Salabim has very minimal requirements (without animation none). 

Salabim runs under Windows, MacOS and Linux, iOS/iPadOS (Pythonista) and can be used with "Python In Excel".

See www.salabim.org for details. 

See www.salabim.org/manual for the documentation.
"""

setup(
    name="salabim",
    packages=["salabim"],
    version="23.3.10",
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

