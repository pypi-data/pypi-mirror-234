import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wt_mqtt",
    version="2.0.1",
    author="xiaoboplus",
    author_email="xiaoboplus@waveletplus.com",
    description="WaveletThings Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['jsonschema>=3.2.0', 'paho-mqtt>=1.5.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
