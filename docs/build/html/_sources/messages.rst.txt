Messages
===============
The methods available in the Messages module give you the ability to list the messages in your global or user library, and
to get a messages name, category, and ID.

List Messages
#################
.. automethod:: QualtricsAPI.Library.messages.Messages.list_messages

Example Implementation
----------------------
Here is an example on how to implement the list_messages() method, which is a method that list all the messages available
to a user within a specified library. Here we call the list_messages method and pass in either a global or user library as
an argument to the library parameter.
::
    #Setup your Credentials, if not already done.
    #You only have to do this once.

    #Import the module
    from QualtricsAPI.Library import Messages

    #Create an instance
    m = Messages()

    #Call the method
    m.list_messages(library="GR_ThisIsaFakeID!!")

This will return a Pandas DataFrame like the one below.
::

                 MessageID        MessageDescription MessageCategory           LibraryID
    0   MS_ThisIsMSFakeID1             Survey-Invite          invite  GR_ThisIsaFakeID!!
    1   MS_ThisIsMSFakeID2           Survey-Reminder          invite  GR_ThisIsaFakeID!!


Get a Message
#################
.. automethod:: QualtricsAPI.Library.messages.Messages.get_message

Example Implementation
-----------------------
Here is an example on how to implement the get_message() method, which is returns three pieces of information about a
given message.
::
    #Setup your Credentials, if not already done.
    #You only have to do this once.

    #Import the module
    from QualtricsAPI.Library import Messages

    #Create an instance
    m = Messages()

    #Call the method
    m.get_message(library="GR_ThisIsaFakeID!!", message="MS_ThisIsMSFakeID2")

Calling this method will return a tuple containing three pieces of information about the message. It contains the
message ID, the Message Category (invite, reminder, etc.), and the Message Name.
::
    (MS_ThisIsMSFakeID2, reminder, Survey-Reminder)
