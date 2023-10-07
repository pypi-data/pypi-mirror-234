Version
=======

.. toctree::
   :hidden:

   get_version


Introduction
------------

Versioning is a process for designating the development stages of the API through unique incremental identifiers. In distinguishing and logging the state of the API at a given point in time, a version numbering scheme enables detailed sequencing and easy tracking of all new developments and iterations. An iterative API name also acts as a check mechanism for verifying the client application's compatibility with the latest version.


Version Numbering
-----------------

Similar to Apache and Semantic, versions are denoted using a standard triplet of integers: ``major.minor.patch``. Each of these variables represents a varying degree of change to the API, and will increment based on the nature of new developments.

- The ``major`` versions entail incompatible, large-scale upgrades or drastic revamping of the code.

- The ``minor`` versions retain source and binary compatibility with older versions, and are incremented with substantial new functionality, modifications, and/or significant fixes [#]_.

- The ``patch`` versions are perfectly compatible, forwards and backwards, and only incremented in the case of backwards compatible bug fixes being introduced. A bug fix is defined as an internal change that fixes incorrect behavior.

.. [#] "Source compatible" means that an application will continue to build without error, and that semantics will remain unchanged. "Binary compatible" to mean that a compiled application can be linked (possibly dynamically) with the library and continue to function properly.

References:

- Apache Portable Runtime (APR)'s Version Numbering (http://apr.apache.org/versioning.html)
- Semantic Versioning (http://semver.org/)
- PEP 386 - Changing the version comparison module in Distutils (http://www.python.org/dev/peps/pep-0386/)


Resources
---------

- :doc:`get_version`
