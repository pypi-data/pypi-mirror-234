``GET /version``
================

Synopsis
--------

Return the current version of the API deployed on the requested environment stage.  This enables a check of the client application against the latest version of the API to ensure compatibility.  If there is a discrepancy between the two, the client application is prompted to update accordingly.

The client application verifies compatibility with the latest API version through comparing its sequence identifier, which follows the form of ``major.minor.patch``.  These four variables represent the degree of modifications to the API, and will increment based on the nature of new developments.


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

The service returns a JSON data structure representing the current version of the API::

    {
      "major": integer,
      "minor": integer,
      "patch": integer
  }

where:

- ``major``: This number identifies the product stage of the project.  The basic intent is that ``major`` versions are incompatible, large-scale upgrades of the software component.  This enables a check of a client application against the latest version of the software component to ensure compatibility.  If there is a discrepancy between the two, the client application MUST be updated accordingly.

- ``minor``: This number is incremented when substantial new functionality or improvement are introduced; the ``major`` version number doesn't change.  A ``minor`` version retains backward compatibility with older minor versions.  It is NOT forward compatible as a previous ``minor`` version doesn't include new functionality or improvement that has been introduced in this newer ``minor`` version [#]_.

- ``patch``: This number is incremented when bugs were fixed or   implementation details were refactored.  The ``major`` and ``minor`` version don't change.  A ``patch`` version is backward
  and forward compatible with older and newer patches of the same major and minor version.

If the client application detects that it is not compatible with the platform version, it must alert the user and invite them to update accordingly (this should be done automatically). If the user does not accept an update, the client application must halt its execution.

.. [#] "Source compatible" means that an application will continue to build without error, and that semantics will remain unchanged. "Binary compatible" to mean that a compiled application can be linked (possibly dynamically) against the library and continue to function properly.
