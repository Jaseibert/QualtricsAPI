import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='QualtricsAPI',
    version='0.1.3',
    author='Jeremy A. Seibert',
    author_email='Jaskzc@mail.missouri.edu',
    description="QualtricsAPI is a lightweight Python library for the Qualtrics Web API. ",
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
