import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "iosense_connect",
    version = "4.0.7",
    author = "Faclon-Labs",
    author_email = "reachus@faclon.com",
    description = "iosense connect library",
    packages = ["iosense_connect"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires=[
        'cryptography>=41.0',
        'fsspec>=2023.6',
        'numpy>=1.24',
        'pandas>=2.0',
        'python_dateutil>=2.8',
        'Requests>=2.31',
        'urllib3>=1.26',
        'pyarrow',
        'azure-storage-blob>=12.16',
        'adlfs>=2023.4',
        'azure-core>=1.27',
        'azure-datalake-store>=0.0',
        'azure-identity>=1.13',
        'botocore>=1.29',
        'gcsfs>=2023.6',
        's3fs>=2023.6',
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
