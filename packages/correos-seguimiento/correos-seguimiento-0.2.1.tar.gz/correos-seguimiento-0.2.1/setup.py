# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open("README.md") as f:
    README = f.read()


VERSION = "0.2.1"


setup(
    name="correos-seguimiento",
    version=VERSION,
    author="Coopdevs, Som Connexio",
    author_email="info@coopdevs.org",
    maintainer="Daniel Palomar, Gerard Funosas, César López",
    url="https://git.coopdevs.org/coopdevs/som-connexio/correos/correos-seguimiento",
    description="Python wrapper for Correos Seguimiento JSON API",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "docs")),
    include_package_data=True,
    zip_safe=False,
    install_requires=["requests"],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        "Operating System :: POSIX :: Linux",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
