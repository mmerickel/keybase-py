keybase-py
==========

This is just a fun little library to see how to generate a cookie-based
session for https://keybase.io. The API documentation is at
https://keybase.io/__/api-docs/1.0.

Installation
------------

This was made using Python 3.4, if you are on a different version of Python
you probably will need to install setuptools/pip yourself.

Clone the repository::

  git clone https://github.com/mmerickel/keybase-py.git
  cd keybase-py

Create a virtualenv::

  export VENV=env # a useful variable for the path to the virtualenv
  pyvenv $VENV
  $VENV/bin/pip install -e .

Usage
-----

Upload a public key::

  $VENV/bin/keybase -l mmerickel --pubkey-file 56B829E5.asc
  Password: ********
