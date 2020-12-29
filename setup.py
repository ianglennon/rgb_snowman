import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpi_RGBSnowman",
    version="0.0.1",
    author="glennog",
    author_email="ianglennon@gmail.com",
    description="A small package to drive an RGB LED",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ianglennon/snowman",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
