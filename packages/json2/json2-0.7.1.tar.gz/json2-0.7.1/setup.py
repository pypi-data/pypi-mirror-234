import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="json2",
    version="0.7.1",
    author="Adrian Thoenig",
    description="Add convenience function to pythons default json implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThoenigAdrian/json2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.5',
    setup_requires=['wheel'],
)
