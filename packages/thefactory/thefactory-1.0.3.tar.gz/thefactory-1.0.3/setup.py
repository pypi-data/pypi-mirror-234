import setuptools

with open("thefactory/README.md", "r") as fh:
    long_description = fh.read()

with open("thefactory/requirements.txt", "r") as req_file:
    required_modules = req_file.read().splitlines()

setuptools.setup(
    name="thefactory",
    version="1.0.3",
    author="Laurie McIntosh",
    author_email="laurie.mcintosh@mimeanalytics.com",
    description="TheFactory config module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/laurielounge/thefactory_module",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=required_modules,
    py_modules=['config', 'google_configv4', 'google_analytics', 'factory_utilities'],
)
