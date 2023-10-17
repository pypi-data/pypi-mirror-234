import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="formant",
    version="1.140.31",
    author="Formant",
    author_email="eng@formant.io",
    description="Formant python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://formant.io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "grpcio>=1.37.0",
        "grpcio-status>=1.37.0",
        'protobuf==3.17.3; python_version<"3.0.0"',
        'protobuf>=3.15.8, <=3.19.5; python_version>="3.0.0"',
        "typing-extensions>=3.7.4.2",
        "requests>=2.25.1",
        "python-lzf>=0.2.4",
        "jsonschema>=1.0.0",
        "python-dateutil",
        "httpx; python_version>='3.0.0'",
        "numpy>=1.16.6",
    ],
    python_requires=">=2.7",
)
