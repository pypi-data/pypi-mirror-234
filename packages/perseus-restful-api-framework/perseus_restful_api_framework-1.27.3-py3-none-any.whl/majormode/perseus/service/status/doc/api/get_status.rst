``GET /status``
===============

Synopsis
--------

Provide the status of different software components that the platform is built on.


Request Header Fields
---------------------

.. include:: /_include/anonymous_session_header_fields.inc


Request Query Parameters
------------------------

None.


Request Message Body
--------------------

None.


Response Message Body
---------------------

The service returns the following JSON data::

    [
      {
        "name": string,
        "status": boolean,
        "check_duration": timestamp,
        "error": string
      },
      ...
    ]

where:

* ``name``: name of the software component.

* ``status``: boolean value that indicates whether the component is available.

* ``check_duration``: duration, expressed in milliseconds, of the check.

* ``error``: possible error detected by the method responsible for checking this component.


Exceptions
----------

None.
