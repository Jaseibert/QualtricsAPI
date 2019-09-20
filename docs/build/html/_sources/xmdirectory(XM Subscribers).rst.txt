XM Directory (XM Subscribers)
=======================================
The methods in the XMDirectory module give you the ability to create contacts,
delete contacts, list contacts, get a contact's information, get the additional information about a contact all from
the XMDirectory.


Create a Contact in the XMDirectory
#######################################
.. automethod:: QualtricsAPI.XM.xmdirectory.XMDirectory.create_contact_in_XM

Example Implementation
----------------------
Here is an example on how to implement the create_contact_in_XM() method. We will create a contact named John Smith in our
XMDirectory.
::
    #Setup your Credentials, if not already done.
    #You only have to do this once.

    #Import the module
    from QualtricsAPI.XM import XMDirectory

    #Create an instance
    x = XMDirectory()

    #Call the method
    x.create_contact_in_XM(first_name='John', last_name='Snow', email='therealking@email.com', phone=None, language="en", metadata={})

This will return John Smith's Contact ID in your XMDirectory.
::
    'CID_FakeContactID'

Delete a Contact in the XMDirectory
#######################################
.. warning::
    Once you delete a contact from the XMDirectory, you will also delete them from any mailing list that the contact is
    associated with. Be sure that you want to implement this!

.. automethod:: QualtricsAPI.XM.xmdirectory.XMDirectory.delete_contact

Example Implementation
----------------------
Here is an example on how to implement the delete_contact() method. Let's say that we no longer want John Smith in our XMDirectory, here
is how we would go about removing him.
::
    #Setup your Credentials, if not already done.
    #You only have to do this once.

    #Import the module
    from QualtricsAPI.XM import XMDirectory

    #Create an instance
    x = XMDirectory()

    #Call the method
    x.delete_contact(contact_id='CID_FakeContactID')

This will return that John Smith's Contact ID has been deleted from your XMDirectory.
::
    'Your XM Contact "CID_FakeContactID" has been deleted from the XM Directory.'

List the Contacts in the XMDirectory
######################################
.. automethod:: QualtricsAPI.XM.xmdirectory.XMDirectory.list_contacts_in_directory

Example Implementation
----------------------
Here is an example on how to implement the list_contacts_in_directory() method. Let's say that we want to pull in the
information from 2 of our contacts in the middle of our XMDirectory. We know that we have 50 people in our XMDirectory.
So we set our offset to 24, because this will start our slice at the 24th contact, and we also set our page_size to 2. Let's
say that we also want this to be returned as a Pandas DataFrame, so we pass True to the 'to_df' parameter (this is the Default Behavior).
::
    #Setup your Credentials, if not already done.
    #You only have to do this once.

    #Import the module
    from QualtricsAPI.XM import XMDirectory

    #Create an instance
    x = XMDirectory()

    #Call the method
    df = x.list_XM_in_directory(page_size=2, offset=24, to_df=True)


This will return a pandas DataFrame containing the 2 contacts from your XMDirectory.
::
               contact_id   first_name last_name                       email phone unsubscribed  language external_ref
    0  CID_FakeContactID1         John      Snow     'therealking@email.com'  None        False      'en'         None
    1  CID_FakeContactID2         Bran     Stark          'b.stark@fake.net'  None        False      None         None


Get a Contacts information from the XMDirectory
##################################################
.. automethod:: QualtricsAPI.XM.xmdirectory.XMDirectory.get_contact

Example Implementation
----------------------
Here is an example on how to call the get_contact() method.
::
    #Setup your Credentials, if not already done.
    #You only have to do this once.

    #Import the module
    from QualtricsAPI.XM import XMDirectory

    #Create an instance
    x = XMDirectory()

    #Call the method
    df = x.get_contact(contact_id='CID_FakeContactID')

    #Print the DataFrames columns
    df.columns

This will return a pandas DataFrame containing the contacts information contained in your XMDirectory. The type of information
will populated the columns below.
::
   Index(['contactId', 'creationDate', 'lastModified', 'firstName', 'lastName',
   'email', 'emailDomain', 'phone', 'language', 'writeBlanks', 'extRef',
   'embeddedData', 'transactionData', 'stats', 'skipped',
   'directoryUnsubscribed', 'directoryUnsubscribeDate',
   'mailingListMembership'])


Get the Additional Information about a Contact in the XMDirectory
####################################################################
.. automethod:: QualtricsAPI.XM.xmdirectory.XMDirectory.get_contact_additional_info

Example Implementation
----------------------
Here is an example on how to call the get_contact_additional_info() method.
::
    #Setup your Credentials, if not already done.
    #You only have to do this once.

    #Import the module
    from QualtricsAPI.XM import XMDirectory

    #Create an instance
    x = XMDirectory()

    #Call the method
    df = x.get_contact_additional_info(contact_id='CID_FakeContactID', content='mailingListMembership')


This will return a pandas DataFrame containing the MailingLists that the contact is on.
::
                     ML_FakeMailingListID
    contactLookupId    MLRP_FakeContactID
    name                       FakeMLName
    unsubscribed                    False
    unsubscribeDate                  None
    ownerId                UR_FakeOwnerID
