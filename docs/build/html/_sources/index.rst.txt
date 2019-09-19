QualtricsAPI Documentation
==========================

`Qualtrics`_ is an awesome company that builds software which gives
users the ability to collect online data through online surveys. This
python package, exists as a wrapper on top of the Qualtrics API. This
package’s primary goal is to be a super convenient way for python users
to ingest, or upload their data from Qualtrics to their development
environment, and vice versa.

Before we continue, I want to mention two things:

First, you must have Qualtrics API access in order to use this package.
Contact whomever your Qualtrics Account Manager is for further clarification
on your account's access credentials.

Secondly, this package is not affiliated with Qualtrics. Thus, I the author of
this package, Jeremy Seibert, is not affiliated with Qualtrics, and Qualtrics
does not offer support for this package. For specific information about the
Qualtrics API, you can refer to their official `documentation`_.

Functionality
-------------

There are currently two primary uses of this package.

There are currently three primary uses of this package.

Contact Data - to manage survey contacts within the XMDirectory and any associated Mailing Lists.

Survey Data - to manage surveys and the data collected from each of your surveys.

Distribution Data - to manage the distributions (i.e. emails) which are sent to contacts as invites, reminders to complete surveys.

R Users
-------

For any R users there is an equally awesome package called
`“qualtRics”`_ which functions in very similar ways to this package. I have
tried to keep consistent with some of the methods that are used in the
qualtRics package and this one, so that there is a cohesion  between the two.
However, I don’t believe that it supports functionality to work within
the Contact Data (i.e. the XMDirectory, or Mailing Lists). `CRAN`_

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   responses
   distributions
   messages
   xmdirectory(XM Subscribers)
   mailinglist(XM Subscribers)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Qualtrics: https://www.qualtrics.com
.. _documentation: https://api.qualtrics.com
.. _“qualtRics”: https://github.com/ropensci/qualtRics
.. _CRAN: 'https://cran.r-project.org/web/packages/qualtRics/index.html'
