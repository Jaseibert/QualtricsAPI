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

For any R users there is an equally awesome package called ["qualtRics"](https://github.com/ropensci/qualtRics) which functions in very similar ways to this package. I have tried to keep consistent with some of the methods that are used in the qualtRics package and this one, so that there is a cohesion between the two. However, I don't believe that it supports functionality to work within the XM Contacts Data (i.e. the XMDirectory, or Mailing Lists). [CRAN]('https://cran.r-project.org/web/packages/qualtRics/index.html')

**Authors:** [Julia Silge](https://juliasilge.com/), [Jasper Ginn](http://www.jasperginn.io)<br/>
**License:** [MIT](https://opensource.org/licenses/MIT)

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

This will generate environment variables that will be used to populate the HTTP headers which are necessary to make your API calls.

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

## Distributions Module

The `Distributions()` module has several useful methods.

```python
from QualtricsAPI.Survey import Distributions

d = Distributions()

# Create send dates
send_in_one_day = d.set_send_date(weeks=0, days=1, hours=0, minutes=0, seconds=0)
send_in_one_week = d.set_send_date(weeks=1, days=0, hours=0, minutes=0, seconds=0)

# Create a Survey Distribution
distribution_id = d.create_distribution(
    subject='Take our survey!',
    reply_email='no-reply@example.com',
    from_email='feedback@example.com',
    from_name='Example Co.',
    mailing_list='<mailing_list_id>',
    library='<library_id>',
    survey='<survey_id>',
    message='<message_id>',
    send_date=send_in_one_day
    link_type='Individual'
)

# Send a Reminder email distribution
d.create_reminder(
    subject='Reminder about your previous survey invitation',
    reply_email='no-reply@example.com',
    from_email='feedback@example.com',
    from_name='Example Co.',
    library='<library_id>',
    message='<message_id>',
    distribution=distribution_id,
    send_date=send_in_one_day
)

# Send a Thank you email
d.create_thank_you(
    subject='Thank you for taking our survey!',
    reply_email='no-reply@example.com',
    from_email='feedback@example.com',
    from_name='Example Co.',
    library='<library_id>',
    message='<message_id>',
    distribution=distribution_id,
    send_date=
)

# Get a list of distributions
d.list_distributions(survey='<survey_id>')

# Get a specific distribution
d.get_distribution(survey='<survey_id>', distribution=distribution_id)

#
d.create_sms_distribution(
    dist_name,
    mailing_list,
    library,
    survey,
    message,
    send_date,
    parentDistributionId=None,
    method='Invite'
)

```

## Survey Module

The `Responses()` module has two methods. Each of those methods can be called using the following methodology.

```python
from QualtricsAPI.Survey import Responses

#Get Survey Responses (Updated)
Responses().get_survey_responses(survey="<survey_id>", verify=None, **kwargs)

#Get Survey Questions (Updated)
Responses().get_survey_questions(survey="<survey_id>", verify=None, **kwargs)
```

# Wrap-up

Again this is currently under development so there may be reduced functionality, but I hope this helps fellow Qualtrics users to expedite their current workflow!

### Want to Contribute?

This project abides by the [Contributor Code of Conduct](CONDUCT.md). By participating in this project you agree to abide by its terms. Feedback, bug reports (and fixes!), and feature requests are welcome!
