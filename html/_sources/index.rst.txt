QualtricsAPI Documentation
==========================

`Qualtrics`_ is an awesome company that builds software which gives
users the ability to collect online data through online surveys. This
python package, exists as a wrapper on top of the Qualtrics API. This
package’s primary goal is to be a super convenient way for python users
to ingest, or upload their data from Qualtrics to their development
environment, and vice versa. I do want to make point to say this package
is not affiliated with Qualtrics, and is an open-source project.

R Users
-------

For any R users there is an equally awesome package called
`“qualtRics”`_ which functions in very similar ways to this package.
However, I don’t believe that it supports functionality to work within
the Contact Data (i.e. the XMDirectory, or Mailing Lists). `CRAN`_

Functionality
-------------

There are currently two primary uses of this package.

1. Contact Data - to manage survey contacts within the XMDirectory and
any associated Mailing Lists.

2. Survey Data - to manage surveys and the data collected from each of
your surveys.

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   responses
   xmdirectory(XM Subscribers)
   mailinglist(XM Subscribers)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Qualtrics: https://www.qualtrics.com
.. _“qualtRics”: https://github.com/ropensci/qualtRics
.. _CRAN: 'https://cran.r-project.org/web/packages/qualtRics/index.html'
