import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='dftools-snowflake',
    packages=setuptools.find_packages(include=['dftools-snowflake']),
    version='0.0.2',
    description='DF-Tools Snowflake',
    author='Lirav DUVSHANI',
    author_email="lirav.duvshani@dataflooder.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache',
    install_requires=[],
    python_requires=">=3.7.9",
)