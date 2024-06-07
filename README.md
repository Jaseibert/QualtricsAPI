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

The `Distributions()` module has methods for creating distributions, reminders, thank you's, SMS distributions, and generating links.

### Distributions
Distributions can be created and fetched with the following methods.
```python
from Qualtrics.Survey import Distributions

# Create a distribution client
distribution_client = Distributions()

# List Distributions for Survey
distribution_list = distribution_client.list_distributions(survey="<Your Survey ID>")

# Create Distribution for Survey
distribution_id = distribution_client.create_distribution(subject="<Email Subject String>", reply_email="<Reply to Email>", from_email="<From Email>",from_name="<From Name>", mailing_list="<Mailing List ID>", library="<Library ID where messages are located>", survey="<Survey ID>", message="<Message ID>", send_date="<DateString of when to send>", link_type="<defaults to individual>")

# Create Reminder for Distribution
reminder_distribution_id = distribution_client.create_reminder(subject="<Email Subject String>", reply_email="<Reply to Email>", from_email="<From Email>",from_name="<From Name>", mailing_list="<Mailing List ID>", library="<Library ID where messages are located>", message="<Message ID>", distribution="<Distribution ID>", send_date="<DateString of when to send>")

# Create Thank-You for Distribution
thank_you_distribution_id = distribution_client.create_thank_you(subject="<Email Subject String>", reply_email="<Reply to Email>", from_email="<From Email>",from_name="<From Name>", mailing_list="<Mailing List ID>", library="<Library ID where messages are located>", message="<Message ID>", distribution="<Distribution ID>", send_date="<DateString of when to send>")
```

### Link Generation

Some users do not wish to send the surveys from Qualtrics, but rather want to generate individual links tied to contacts which will open the survey for that user. The `Distributions()` module contains a method for doing this for a single contact, and for doing it from a dataframe for many contacts (max 10,000 at a time).
```python
import pandas as pd

# Generate Survey Link for single contact
contact_data = { # Sample contact dictionary
    "firstName": 'firstName',
    "lastName": 'lastName',
    "email": 'email@mail.com',
    "phone": '999-555-9999',
    "extRef": 'myexref',
    "unsubscribed": False
}
embedded_data = {"my_key":"my_value"} # Sample Embedded Data object
transactional_data = {"my_key":"my_value"} # Sample Transactional Data object

# The request will return the single link as a string
my_link = distribution_client.generate_individual_survey_link(survey="<Survey ID>", mailing_list="<Mailing List ID>", contact=contact_data, embedded_data=embeddedData, transactional_data=transactionalData, expiration=2) # Where expiration is number of months before link expires (must be >= 1)
print("individual link:",my_link)

# Generate dataframe of links from input dataframe
df = pd.read_csv("path/to/my.csv",na_filter=False) # empty fields being nan will cause error
embedded_data_cols = ['headers','of','embedded fields']
transactional_data_cols ['headers','of','transactional fields']

# The request will return a pandas dataframe containing all contacts and links generated by the API
links_df = distribution_client.generate_links_from_dataframe(survey="<Survey ID>", mailing_list="<Mailing List ID>", df=df, embedded_fields=embedded_data_cols, transactional_fields=transactional_data_cols, expiration=3)
links_df.to_csv("links_table.csv") # Save the DF to file if desired
```

## Survey Module

### Fetch Response Data

The `Responses()` module has two methods for retrieval of response data. Each of those methods can be called using the following methodology.

```python
from QualtricsAPI.Survey import Responses

#Get Survey Responses (Updated)
Responses().get_survey_responses(survey="<survey_id>")

#Get Survey Questions (Updated)
Responses().get_survey_questions(survey="<survey_id>")
```

### Update Response Embedded Data

The `Responses()` module has two methods for updating embedded data on survey responses. `update_survey_response_embedded_data` will update a single response from a dictonary of strings. `bulk_update_many_responses_from_dataframe` will update many responses at once from a pandas dataframe.

```python
from QualtricsAPI.Survey import Responses
import pandas as pd

r = Responses()

# Update a single response from dictionary of strings
new_data = {"my":"new","data":"dictionary"}
r.update_survey_response_embedded_data(survey="<survey_id>", response_id="<response_id>", embedded_data=new_data)

# Update many responses from dataframe
my_df = pd.read_csv("path/to/my/file.csv")
r.bulk_update_many_responses_from_dataframe(survey="<survey_id>", df=my_df,rid_col="<header of response ID column>", update_cols=['headers','of','columns','to be','updated'], chunk_size=100)
```
## Imported Data Project Module

### Get IDP Data

The `ImportedDataProject()` module can be used to retrieve data from imported data projects with the following usage.
```python
from QualtricsAPI.IDP import ImportedDataProject

# Create an instance of our IDP project
idp = ImportedDataProject(idp_source_id="<your idp source id>")

meta, schema = idp.get_idp_schema()

record = idp.get_single_record_from_idp(unique_field=<unique field value of record to be retrieved>)
```

### Create/Update/Delete IDP data

The IDP module includes methods for creating/updating (it will upsert on the unique value) rows into an IDP as both single rows or up to 50 in bulk, as well as a method to delete individual records.
```python
# Add Columns to IDP
new_columns = [{"name":"<new column name 1>","type":"<data type of new field>"}]
column_add_result = idp.add_columns_to_idp(fields=new_cols)

# Create a record from a dictionary
new_record = {"<unique field>":"<value of record>"} 
# keys must match IDP names, values must match type - fetch the schema to see valid inputs
result = idp.add_single_record(record=new_record)

# Create many records from list
new_records = [{"<unique field>":"<value of record1>"},{"<unique field>":"<value of record2>"}]
many_result = idp.add_many_records(records=new_records)

# Delete row from IDP
delete_result = idp.delete_record_from_idp(unique_field='<value of unique field for record to be removed>')
# Value must match type as well
```
the `ImportedDataProject()` module can be imported without a project ID, and IDs can be passed at the time any method is called (`idp_id` is the parameter to set this from a function call). Passing a new id will update the class to this new id. 

# Wrap-up

Again this is currently under development so there may be reduced functionality, but I hope this helps fellow Qualtrics users to expedite their current workflow!

### Want to Contribute?

This project abides by the [Contributor Code of Conduct](CONDUCT.md). By participating in this project you agree to abide by its terms. Feedback, bug reports (and fixes!), and feature requests are welcome!
