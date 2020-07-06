# QualtricsAPI

[![Version](https://img.shields.io/pypi/v/qualtricsapi.svg)](https://pypi.python.org/pypi/qualtricsapi)
[![License](https://img.shields.io/pypi/l/qualtricsapi.svg)](https://pypi.python.org/pypi/qualtricsapi)
[![Python](https://img.shields.io/pypi/pyversions/qualtricsapi.svg)](https://pypi.python.org/pypi/qualtricsapi)
[![Documenation Site](https://img.shields.io/website/https/www.qualtricsapi-pydocs.com.svg?down_color=red&down_message=offline&style=plastic&up_color=green&up_message=online)](https://img.shields.io/website/https/www.qualtricsapi-pydocs.com.svg?down_color=red&down_message=offline&style=plastic&up_color=green&up_message=online)
[![Downloads](https://img.shields.io/pypi/dm/qualtricsapi.svg?style=plastic)](https://img.shields.io/pypi/dm/qualtricsapi.svg?style=plastic)
[![Build Status](https://travis-ci.org/Jaseibert/QualtricsAPI.svg?branch=master)](https://travis-ci.org/Jaseibert/QualtricsAPI)

**Author:** [Jeremy Seibert](https://www.jeremyseibert.com)<br/>
**License:** [MIT](https://opensource.org/licenses/MIT)<br/>
**Package Documentation:** [Documentation](https://www.qualtricsapi-pydocs.com)<br/>


[Qualtrics](https://www.qualtrics.com) is an awesome company that builds software which gives users the ability to collect online data through online surveys. This python package, exists as a wrapper on top of the Qualtrics API. This package's primary goal is to be a super convenient way for python users to ingest, or upload their data from Qualtrics to their development environment, and vice versa.

Before we continue, I want to mention two things:

First, you must have Qualtrics API access in order to use this package. Contact whomever your Qualtrics Account Manager is for further clarification on your account's access credentials.

Secondly, this package is not affiliated with Qualtrics. Thus, I the author of this package, Jeremy Seibert, am not affiliated with Qualtrics, and Qualtrics does not offer support for this package. For specific information about the Qualtrics API, you can refer to their official documentation.

# Functionality

There are currently three primary uses of this package.

1. Contact Data - to manage survey contacts within the XMDirectory and any associated Mailing Lists.

2. Survey Data - to manage surveys and the data collected from each of your surveys.

3. Distribution Data - to manage the distributions (i.e. emails) which are sent to contacts as invites, reminders to complete surveys.

# Basic Usage

## Package Installation

The installation of the package is pretty straight forward. Open up your terminal and run the command below. If you do not already have pip installed on your machine, you may have to install pip first, see [Pip Installation Instructions](https://docs.python.org/3/installing/index.html) for help!

```
$ pip install QualtricsAPI
```

## Credentials Code Flow
We first create environment variables that will hold your API credentials, so you don't have to continually declare them. To do this we import the Credentials module, create and call the `qualtrics_api_credentials()`method.

```python
from QualtricsAPI.Setup import Credentials

#Create an instance of Credentials
c = Credentials()

#Call the qualtrics_api_credentials() method
c.qualtrics_api_credentials(token='Your API Token',data_center='Your Data Center',directory_id='Your Directory ID')
```
This will generate environment variables that will be used to  populate the HTTP headers which are necessary to make your API calls.  

# R Users
For any R users there is an equally awesome package called ["qualtRics"](https://github.com/ropensci/qualtRics) which functions in very similar ways to this package. I have tried to keep consistent with some of the methods that are used in the qualtRics package and this one, so that there is a cohesion  between the two. However, I don't believe that it supports functionality to work within the XM Contacts Data (i.e. the XMDirectory, or Mailing Lists). [CRAN]('https://cran.r-project.org/web/packages/qualtRics/index.html')

**Authors:** [Julia Silge](https://juliasilge.com/), [Jasper Ginn](http://www.jasperginn.io)<br/>
**License:** [MIT](https://opensource.org/licenses/MIT)


### Want to Contribute?

This project abides by the [Contributor Code of Conduct](Conduct.md). By participating in this project you agree to abide by it's terms. Feedback, bugs, any potential fixes, and feature requests are welcome!
