import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tastyigniter",
    version="0.0.6",
    author="Tim Empringham",
    author_email="tim.empringham@live.ca",
    description="Async Python wrapper for TastyIgniter APIs (v26.beta)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/djtimca/tastyigniter-api",
    packages=setuptools.find_packages(),
    keywords=['TastyIgniter'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)