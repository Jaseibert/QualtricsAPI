# QualtricsAPI

[![Build Status](https://travis-ci.com/Jaseibert/QualtricsAPI.svg?branch=master)](https://travis-ci.com/Jaseibert/QualtricsAPI)
![PyPI](https://img.shields.io/pypi/v/QualtricsAPI)
![PyPI - Downloads](https://img.shields.io/pypi/dm/QualtricsAPI)

**Author:** [Jeremy Seibert](https://www.jeremyseibert.com)<br/>
**License:** [MIT](https://opensource.org/licenses/MIT)<br/>
**Package Documentation:** [Documentation](https://www.qualtricsapi-pydocs.com)<br/>


[Qualtrics](https://www.qualtrics.com) is an awesome company that builds software which gives users the ability to collect online data through online surveys. This python package, exists as a wrapper on top of the Qualtrics API. This package's primary goal is to be a super convenient way for python users to ingest, or upload their data from Qualtrics to their development environment, and vice versa.

Before we continue, I want to mention two things:

First, you must have Qualtrics API access in order to use this package. Contact whomever your Qualtrics Account Manager is for further clarification on your account's access credentials.

Secondly, this package is not affiliated with Qualtrics. Thus, I the author of this package, Jeremy Seibert, is not affiliated with Qualtrics, and Qualtrics does not offer support for this package. For specific information about the Qualtrics API, you can refer to their official documentation.

# R Users
For any R users there is an equally awesome package called ["qualtRics"](https://github.com/ropensci/qualtRics) which functions in very similar ways to this package. I have tried to keep consistent with some of the methods that are used in the qualtRics package and this one, so that there is a cohesion  between the two. However, I don't believe that it supports functionality to work within the XM Contacts Data (i.e. the XMDirectory, or Mailing Lists). [CRAN]('https://cran.r-project.org/web/packages/qualtRics/index.html')

**Authors:** [Julia Silge](https://juliasilge.com/), [Jasper Ginn](http://www.jasperginn.io)<br/>
**License:** [MIT](https://opensource.org/licenses/MIT)

# Functionality

There are currently two primary uses of this package.

1. Contact Data - to manage survey contacts within the XMDirectory and any associated Mailing Lists.

2. Survey Data - to manage surveys and the data collected from each of your surveys.

# Basic Usage

## Credentials Code Flow
We first create environment variables that will hold your API credentials, so you don't have to continually declare them. To do this we import the Credentials module, create and call the `qualtrics_api_credentials()`method.

```python
from QualtricsAPI.Setup import Credentials

#Call the qualtrics_api_credentials() method (Non-XM Directory Users)
Credentials().qualtrics_api_credentials(token='Your API Token',data_center='Your Data Center')

#Call the qualtrics_api_credentials() method (XM Directory Users)
Credentials().qualtrics_api_credentials(token='Your API Token',data_center='Your Data Center',directory_id='Your Directory ID')


```
This will generate environment variables that will be used to  populate the HTTP headers which are necessary to make your API calls.  

## Contact Data

Now the generation of the necessary HTTP headers will be handled automatically, so we don't have to worry about it. We have 2 modules available to work with Contact Data. The first is `XMDirectory()`, and `MailingList()`. We import each as follows below.

```python
from QualtricsAPI.XM import XMDirectory
from QualtricsAPI.XM import MailingList

#Create instances of each
x = XMDirectory()
m = MailingList()
```
Once imported, there are 10 methods that are available between both modules.

1. XMDirectory() Class Methods

```python
# Creates contacts in the XMDirectory
x.create_contact_in_XM()

#Deletes a contact in the XMDirectory (use cautiously!)
x.delete_contact()

#lists Contacts in the XMDirectory
x.list_contacts_in_directory()
```

2. MailingList() Class Methods

```python
#Creates a new Mailing list for the given Qualtrics User()
m.create_list()

#Lists the Mailing Lists for the given Qualtrics User()
m.list_lists()

#Gets the Attributes of the defined Mailing List
m.get_list()

#Renames the defined Mailing List
m.rename_list()

#Deletes a defined Mailing List (use cautiously!)
m.delete_list()

#Lists the contacts in the defined Mailing List
m.list_contacts()

#Creates contacts in a Mailing List
m.create_contact_in_list()
```
## Survey Data

There is currently only one module built to work with the Survey Data, `Responses()`. This modules has one method which downloads the responses associated with a given survey. That method can be called using the following methodology.

```python
from QualtricsAPI.Surveys import Responses

#Create instances of each
r = Responses()

#Call the method
r.get_responses()
```

# Wrap-up

Again this is currently under development so there may be reduced functionality, but I hope this helps fellow Qualtrics users to expedite their current workflow!

### Want to Contribute?

This project abides by the [Contributor Code of Conduct](CONDUCT.md). By participating in this project you agree to abide by its terms. Feedback, bug reports (and fixes!), and feature requests are welcome!
