from setuptools import find_namespace_packages
from setuptools import setup


version = "3.0.3"

setup(
    name="mauritstestpackage2",
    version=version,
    description="Test package from Maurits for uploading to PyPI.",
    long_description=(open("README.rst").read() + "\n\n" + open("CHANGES.rst").read()),
    # Get strings from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="test release pypi",
    author="Maurits van Rees",
    author_email="maurits@vanrees.org",
    url="https://github.com/mauritsvanrees/mauritstestpackage",
    license="GPL",
    packages=find_namespace_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
    ],
    entry_points="""
      # -*- Entry points: -*-
      """,
)
