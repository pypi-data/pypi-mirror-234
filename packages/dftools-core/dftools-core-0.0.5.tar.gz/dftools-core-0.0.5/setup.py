import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='dftools-core',
    packages=setuptools.find_namespace_packages(include=['dftools']),
    version='0.0.5',
    description='Data Flooder Tools - Core Package',
    author='Lirav DUVSHANI',
    author_email="lirav.duvshani@dataflooder.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache',
    install_requires=[],
    python_requires=">=3.7.9",
)