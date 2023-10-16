import setuptools
with open("./README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="common-web",
    version="0.1.4",
    author="Cloud Bian",
    author_email="cloudbian@139.com",
    description="this is common for base",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)