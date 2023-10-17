import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mvsdk',
    version='0.0.6-2310111200',
    author='James Armstrong',
    author_email='j@armstro.ca',
    description='MediaValet Python SDK',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/armstro-ca/mvsdk',
    project_urls={
        "Bug Tracker": "https://github.com/armstro-ca/mvsdk/issues"
    },
    license='MIT',
    packages=setuptools.find_packages(where='src'),
    install_requires=['requests'],
    package_dir={'': 'src'},
)