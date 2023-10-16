Flask-Security-Invenio
======================

.. warning::

    Please do not use this fork. Use `Flask-Security-Too instead <https://flask-security-too.readthedocs.io/en/stable/>`_.

This is a fork is used exclusively for Invenio Framework. The fork has been
considerably slimmed down removing unused features to lower the  attack
surface. In addition, Invenio Framework delegates most authentication to
identity providers and thus do not need advanced features such as multi factor
authentication which was added in Flask-Security-Too.

The following features have been **removed** from the original Flask-Security:

- Basic HTTP authentication
- Token based authentication
- JSON/Ajax Support
- MongoDB, PonyORM and Peewee support.

Flask-Security-Invenio uses the following other libraries:

1. `Flask-Login <https://flask-login.readthedocs.org/en/latest/>`_
2. `Flask-Mail <http://packages.python.org/Flask-Mail/>`_
3. `Flask-Principal <http://packages.python.org/Flask-Principal/>`_
4. `Flask-WTF <http://packages.python.org/Flask-WTF/>`_
5. `itsdangerous <http://packages.python.org/itsdangerous/>`_
6. `passlib <http://packages.python.org/passlib/>`_

.. include:: contents.rst.inc
