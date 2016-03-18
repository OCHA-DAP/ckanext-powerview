.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/OCHA-DAP/ckanext-powerview.svg?branch=master
    :target: https://travis-ci.org/OCHA-DAP/ckanext-powerview

.. image:: https://coveralls.io/repos/OCHA-DAP/ckanext-powerview/badge.svg
  :target: https://coveralls.io/r/OCHA-DAP/ckanext-powerview


=================
ckanext-powerview
=================

Data source and configuration to power a view for one or more resources.


------------
Requirements
------------

Requires CKAN 2.3+


------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-powerview:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-powerview Python package into your virtual environment::

     pip install ckanext-powerview

3. Install dependencies::

     pip install -r requirements.txt

4. Create the database tables::

     paster --plugin=ckanext-powerview powerview init --config=production.ini

5. Add ``powerview`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

6. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


------------------------
Development Installation
------------------------

To install ckanext-powerview for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/OCHA-DAP/ckanext-powerview.git
    cd ckanext-powerview
    python setup.py develop
    pip install -r requirements.txt
    pip install -r dev-requirements.txt


---
API
---

All actions in the PowerView extension are available in the CKAN Action API.

PowerView actions::

    - create a new powerview (sysadmins only)
    curl -X POST http://127.0.0.1:5000/api/3/action/powerview_create -H "Authorization:{YOUR-API-KEY}" -d '{"title": "My New View", "view_type": "my-view-type"}'

    - update an existing powerview (sysadmins only)
    curl -X POST http://127.0.0.1:5000/api/3/action/powerview_update -H "Authorization:{YOUR-API-KEY}" -d '{"id":"my-powerview-id", "title": "My Updated Title", "view_type": "my-view-type"}'

    - delete a powerview (sysadmins only)
    curl -X POST http://127.0.0.1:5000/api/3/action/powerview_delete -H "Authorization:{YOUR-API-KEY}" -d '{"id": "my-powerview-id"}'

    - show a powerview
    curl -X POST http://127.0.0.1:5000/api/3/action/powerview_show -d '{"id": "my-powerview-id"}'

    - list resources in a powerview
    curl -X POST http://127.0.0.1:5000/api/3/action/powerview_resource_list -d '{"id": "my-powerview-id"}'

    - add a resource to an existing powerview (sysadmins only)
    curl -X POST http://127.0.0.1:5000/api/3/action/powerview_add_resource -d '{"id": "my-powerview-id", "resource_id": "my-resource-id"}'

    - remove a resource to an existing powerview (sysadmins only)
    curl -X POST http://127.0.0.1:5000/api/3/action/powerview_remove_resource -d '{"id": "my-powerview-id", "resource_id": "my-resource-id"}'



-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.powerview --cover-inclusive --cover-erase --cover-tests


-------------------------------------
Registering ckanext-powerview on PyPI
-------------------------------------

ckanext-powerview should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-powerview. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


--------------------------------------------
Releasing a New Version of ckanext-powerview
--------------------------------------------

ckanext-powerview is availabe on PyPI as https://pypi.python.org/pypi/ckanext-powerview.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
