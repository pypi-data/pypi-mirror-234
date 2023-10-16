import setuptools

with open(r"README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythttp",
    version="0.2.0",
    author="Example Author",
    author_email="team.longinus.project@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/projectlonginus/httpy",
    install_requires=['dataclasses','datetime','uuid'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.11',
)