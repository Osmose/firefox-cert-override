firefox-cert-override
=====================
.. image:: https://circleci.com/gh/Osmose/firefox-cert-override.svg?style=svg
   :target: https://circleci.com/gh/Osmose/firefox-cert-override

``firefox-cert-override`` is a Python library and CLI utility for reading and writing ``cert_override.txt`` files.

``cert_override.txt`` is located at the root of a Firefox profile directory and stores the per-domain certificate overrides for that profile. When you permanently add an exception for Firefox to trust a certificate for a specific domain, Firefox adds an entry to ``cert_override.txt``, and will read it on startup in the future to load the override again.

Installation
------------
``firefox-cert-override`` requires (read: has only been tested on) Python 3.5.
::

   $ pip install firefox-cert-override

API
---
There isn't any documentation for the API (yet), but ``firefox_cert_override/base.py`` is where the main functionality lives and is a quick skim.

CLI
---
The package adds a ``firefox-cert-override`` command that takes a list of domain and certificate file path pairs and outputs the contents for a ``cert_override.txt`` file with overrides for the given domains. See ``firefox-cert-override --help`` for more details.

License
-------
Licensed under the MIT License. See ``LICENSE`` for details.
