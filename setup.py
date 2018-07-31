import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="storelocator",
    version="1.0.5",
    author="Austin Brown",
    author_email="austinbrown34@gmail.com",
    description="Command-line tool to find nearest store.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/austinbrown34/StoreLocator",
    packages=setuptools.find_packages(),
    scripts=['scripts/find_store'],
    install_requires=[
        'geocoder>=1.38.1',
        'nose2>=0.7.4',
        'numpy>=1.15.0',
        'scipy>=1.1.0'
    ],
    include_package_data=True
)
