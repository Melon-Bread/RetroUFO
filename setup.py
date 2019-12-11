import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RetroUFO", # Replace with your own username
    version="0.9.5",
    author="Melon Bread",
    author_email="rain@melonbread.dev",
    description="Easily upgrade all libreto cores from the build bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords=["libretro", "retroarch", "core"],
    url="https://github.com/pypa/sampleproject",
    packages=["RetroUFO"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)