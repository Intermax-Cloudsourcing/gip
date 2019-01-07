import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(
    name='gip',
    version='0.1',
    scripts=['gip'],
    author="Wilmar den Ouden",
    author_email="wilmaro@intermax.nl",
    description="A language agnostic dependency manager on top of the Gitlab API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
