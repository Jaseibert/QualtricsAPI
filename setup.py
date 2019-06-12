import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='QualtricsAPI',
    version='0.1.1',
    author='Jeremy A. Seibert',
    author_email='Jaskzc@mail.missouri.edu',
    description="This is wrapper is a convenient way for python users to ingest, or upload their data from Qualtrics to their development environment.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jaseibert/QualtricsAPI",
    license='MIT',
    packages=setuptools.find_packages(),
    keywords='qualtrics api python',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
