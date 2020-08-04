import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='QualtricsAPI',
    version='0.3.2',
    author='Jeremy A. Seibert',
    author_email='jeremy@seibert.industries',
    description="QualtricsAPI is a lightweight Python library for the Qualtrics Web API. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jaseibert/QualtricsAPI",
    license='MIT',
    packages=setuptools.find_packages(),
    keywords='qualtrics api python research survey',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'pandas',
          'numpy',
          'requests'
      ],
)
