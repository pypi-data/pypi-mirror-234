from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="ds20kdb-avt",
    version="0.2.0",
    author="Alan Taylor",
    author_email="avt@hep.ph.liv.ac.uk",
    maintainer="Alan Taylor",
    maintainer_email="avt@hep.ph.liv.ac.uk",
    description="Python interface to the DarkSide-20k pre-production database and automation scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="",
    url="https://gitlab.in2p3.fr/darkside/productiondb_software/",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "importlib-metadata",
        "opencv-python",
        "pandas",
        "python-dateutil",
        "pyzbar",
        "requests",
        "ttkwidgets",
        "paramiko",
    ],
    entry_points={
        "console_scripts": [
            "create_credentials_file = ds20kdb.create_credentials_file:main",
            "dsqr = ds20kdb.qr:main",
            "submit_vtile = ds20kdb.submit_vtile:main",
            "ds20k_create_credentials_file = ds20kdb.create_credentials_file:main",
            "ds20k_qrgen = ds20kdb.qrgen:main",
            "ds20k_read_qrcode = ds20kdb.qr:main",
            "ds20k_scanner_auto = ds20kdb.scanner_auto:main",
            "ds20k_submit_cr_test_result = ds20kdb.vtile_test_submit_cr:main",
            "ds20k_submit_vtile = ds20kdb.submit_vtile:main",
            "ds20k_wafer_map_from_db = ds20kdb.wafer_map_from_db:main",
        ]
    },
    # see https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Environment :: Console",
        "Environment :: X11 Applications",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
)
