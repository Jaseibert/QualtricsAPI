Mailing Lists (XM Subscribers)
====================================
The methods in the MailingList module give you the ability to create create new mailing lists,
delete mailing lists, list all of the available mailing lists to your user account, get a Mailing List's information,
rename a Mailing List, list all of the contacts in a mailing list, and create a new contact within a mailing list.

Create a Mailing List
######################
.. automethod:: QualtricsAPI.XM.mailinglists.MailingList.create_list

Example Implementation
----------------------
Here is an example on how to implement the create_list() method. We will create a new mailing list called 'MyNewMailingList' that
will be available to your specific user's account.
::
    #Setup your Credentials, if not already done.
    #You only have to do this once.

    #Import the module
    from QualtricsAPI.XM import MailingList

    #Create an instance
    m = MailingList()

    #Call the method
    m.create_list(name='MyNewMailingList')

This will return a tuple containing the new mailing list's name, and the Mailing List ID associated with the new Mailing List.
::
    ('MyNewMailingList', 'CG_FakeMailingListID')

List the Mailing Lists Available to your Account
####################################################
.. automethod:: QualtricsAPI.XM.mailinglists.MailingList.list_lists

Example Implementation
----------------------
Here is an example on how to implement the list_lists() method. Let's say that we want to pull in the
information from 2 of our Mailing Lists at the start of the list of Mailing Lists. Thus, we set our offset to 0, and
the page_size to 2. Let's say that we also want this to be returned as a Pandas DataFrame, so we pass True to the 'to_df'
parameter (this is the Default Behavior)
::
    #Setup your Credentials, if not already done.
    #You only have to do this once.

    #Import the module
    from QualtricsAPI.XM import MailingList

    #Create an instance
    m = MailingList()

    #Call the method
    m.list_lists(page_size=2, offset=0, to_df=True)

This method when implemented and the argument passed to the parameter 'to_df' is True, will return a Pandas DataFrame
that will look like the following.
::
               mailingListId               name         ownerId       lastModifiedDate         creationDate contactCount
    0  CG_FakeMailingListID1  MyNewMailingList1  UR_FakeUserID1    2017-03-04 14:22:36  2017-02-30 21:32:36          100
    1  CG_FakeMailingListID2  MyNewMailingList2  UR_FakeUserID1    2018-05-30 21:32:36  2018-02-15 21:32:31           10

Get the Information about a Mailing List
#########################################
.. automethod:: QualtricsAPI.XM.mailinglists.MailingList.get_list

Example Implementation
----------------------
The get list method gives you the ability to get the same information about a Mailing List as you would receive from the list_lists()
method, except it is for a singular Mailing List.

::
    #Setup your Credentials, if not already done.
    #You only have to do this once.

    #Import the module
    from QualtricsAPI.XM import MailingList

    #Create an instance
    m = MailingList()

    #Call the method
    m.get_list(mailing_list='CG_FakeMailingListID')

This method will return a Pandas DataFrame containing information specific to the mailing list that was passed.
::
               mailingListId               name         ownerId      lastModifiedDate         creationDate contactCount
    0  CG_FakeMailingListID1  MyNewMailingList1  UR_FakeUserID1   2018-05-30 21:32:36  2018-02-15 21:32:31          100

Rename a Mailing List
#########################
.. automethod:: QualtricsAPI.XM.mailinglists.MailingList.rename_list

Example Implementation
----------------------
The rename_list method gives you the ability to rename one of your Mailing Lists. Here we will rename our mailing list with the
ID 'CG_FakeMailingListID', and rename it to 'NewNamedMList'.
::
    #Setup your Credentials, if not already done.
    #You only have to do this once.

    #Import the module
    from QualtricsAPI.XM import MailingList

    #Create an instance
    m = MailingList()

    #Call the method
    m.rename_list(mailing_list='CG_FakeMailingListID', name='NewNamedMList')

If you have successfully renamed the mailing list, you will be returned the following message.
::
    'Your mailing list "CG_FakeMailingListID" has been renamed to "NewNamedMList" in the XM Directory.'

Delete a Mailing List
#########################
.. automethod:: QualtricsAPI.XM.mailinglists.MailingList.delete_list

.. warning::
    Once deleted this cannot be undone, be sure that you want to implement this!

Example Implementation
----------------------
The delete_list method gives you the ability to delete one of your Mailing Lists. Here we will delete the mailing list with
the ID 'CG_FakeMailingListID'. We simply pass the ID of the mailing list to the method, and the associated list will be
deleted.

::
    #Setup your Credentials, if not already done.
    #You only have to do this once.

    #Import the module
    from QualtricsAPI.XM import MailingList

    #Create an instance
    m = MailingList()

    #Call the method
    m.delete_list(mailing_list='CG_FakeMailingListID')

If you have successfully deleted the mailing list, you will be returned the following message.
::
    'Your mailing list "CG_FakeMailingListID" has been deleted from the XM Directory.'

List the Contacts in a Mailing List
######################################
.. automethod:: QualtricsAPI.XM.mailinglists.MailingList.list_contacts

Example Implementation
----------------------
In this example lets say that we want to print out the first two contacts within our mailing list with the
ID, 'CG_FakeMailingListID' and we want to return the information in a pandas DataFrame.
::
    #Setup your Credentials, if not already done.
    #You only have to do this once.

    #Import the module
    from QualtricsAPI.XM import MailingList

    #Create an instance
    m = MailingList()

    #Call the method
    m.list_contacts(mailing_list='CG_FakeMailingListID', page_size=2, offset=0, to_df=True)

When called you will return a DataFrame that will look like the one below.
::
               contact_id   first_name last_name                       email phone unsubscribed  language external_ref
    0  CID_FakeContactID1         John      Snow     'therealking@email.com'  None        False      'en'         None
    1  CID_FakeContactID2         Bran     Stark          'b.stark@fake.net'  None        False      None         None

Create a Contact in a Mailing List
####################################
.. warning::
    When you create a contact using the create_contact_in_list method, you will also create a record in the XM Directory. This
    process can lead to duplications of contacts within your XM Directory. Refer to the `Manage Directory Duplicates <https://www.qualtrics.com/support/iq-directory/directory-contacts-tab/directory-options/>`_
    page of the Qualtrics Documentation.

.. automethod:: QualtricsAPI.XM.mailinglists.MailingList.create_contact_in_list

Example Implementation
----------------------
Here we will learn how to create a new contact within a specific mailing list. Let's say that we want to create a contact
named John Smith, in our mailing list with the ID 'CG_FakeMailingListID'. We pass all of the parameters that we deem necessary to the
John Smith, and then create a record of him in the mailing list (and implicitly in the XMDirectory).
::
    #Setup your Credentials, if not already done.
    #You only have to do this once.

    #Import the module
    from QualtricsAPI.XM import MailingList

    #Create an instance
    m = MailingList()

    #Call the method
    m.create_contact_in_list(mailing_list='CG_FakeMailingListID', first_name='John', last_name='Snow', email='therealking@email.com', phone=None, language="en")

If successful, you will be returned a tuple containing John Snow's new contact_id (ie. the reference in the XMDirectory) and his contact_list_id
(i.e. the reference in the specified Mailing List)
::
    ('CID_FakeContactID','')
