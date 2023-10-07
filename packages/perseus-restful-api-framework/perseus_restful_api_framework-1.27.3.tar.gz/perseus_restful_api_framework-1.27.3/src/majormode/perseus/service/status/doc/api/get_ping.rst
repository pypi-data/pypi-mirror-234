=============
``GET /ping``
=============

--------
Synopsis
--------

Provide a simple mechanism to help developers or other remote services
ensure that their software is interacting correctly with the web
services infrastructure, to measure the round-trip time for requests
sent from the local host to the Web services server.


---------------------
Request Header Fields
---------------------

.. include:: /_include/anonymous_session_header_fields.inc


------------------------
Request Query Parameters
------------------------

None.


--------------------
Request Message Body
--------------------

None.


---------------------
Response Message Body
---------------------

The platform returns the following JSON data::

   {
     "data": "pong"
   }


----------
Exceptions
----------

None.
