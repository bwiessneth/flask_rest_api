##############
Flask REST API
##############

Basic REST API using Flask, Flask-RESTful, Flask-Marshmallow, and Flask-SQLAlchemy.

All endpoints will return JSON formatted output.



Users
=====

The ``/users`` endpoint provides the User ressource.

=========== =========== =======================
HTTP Method URI         Action
=========== =========== =======================
GET         /users      Retrieve list of users
GET         /users/[id] Retrieve a user
POST        /users      Create a new user
PUT         /users/[id] Update an existing user
DELETE      /users/[id] Delete a user
=========== =========== =======================



Departments
===========

The ``/departments`` endpoint provides the Department ressource.

=========== ================= =============================
HTTP Method URI               Action
=========== ================= =============================
GET         /departments      Retrieve list of departments
GET         /departments/[id] Retrieve a department
POST        /departments      Create a new department
PUT         /departments/[id] Update an existing department
DELETE      /departments/[id] Delete a department
=========== ================= =============================



**********
Pagination
**********

All endpoints that return a list of entities support pagination.

Parameter
=========

For controlling the pagination there are currently two paramters in place.
Both paramters can be passed as URL parameters (e.g. ``api/v0/users?limit=5&offset=2``).

* ``limit``: Number of requested results per response/page
* ``offset``: Offset of requested results



Response format
===============

Every endpoint which supports pagination is indicating this by returning some info about its size.

* ``total``: Total number of entities within the ressource

.. code-block:: javascript

{
    "offset": 2,
    "limit": 5,
    "total": 21,
    "data": [..]
}





********************
TODO: Authentication
********************



****************
TODO: Rate limit
****************


*************
TODO: Testing
*************
