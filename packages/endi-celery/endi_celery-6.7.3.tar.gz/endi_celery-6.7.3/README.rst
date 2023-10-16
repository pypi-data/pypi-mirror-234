enDI asynchronous tasks
============================

Since version 6, endi-celery only supports python 3.

Asynchronous tasks are executed through celery.
pyramid_celery is used to integrate celery with the Pyramid related stuff.
pyramid_beaker is used to cache responses.

tasks:

    Asynchronous tasks called from enDI

scheduler:

    Beat tasks, repeated along the time (like cron tasks)

Results
-------

No result backend is used, tasks interact directly with enDI's database to
return datas.

enDI celery provides all the models that should be used to store task
execution related stuff (see endi_celery.models).

Install
-------

System packages
................

autonmie_celery needs a redis server to run

On Debian

.. code-block:: console

    apt-get install redis-server


On Fedora

.. code-block:: console

    dnf install redis-server

Python stuff
.............

endi_celery should be run in the same environment as enDI :
https://framagit.org/endi/endi

You may first run

.. code-block:: console

    workon endi


.. code-block:: console

    git clone https://framagit.org/endi/endi_celery.git
    cd endi_celery
    python setup.py install
    cp development.ini.sample development.ini

Customize the development.ini file as needed


Start it
---------

Launch the following command to launch the worker daemon::

    celery worker -A pyramid_celery.celery_app  --ini development.ini

Launch the following command to launch the beat daemon::

    celery beat -A pyramid_celery.celery_app --ini development.ini


Customize accounting operation parser and producer for different general_ledger files
---------------------------------------------------------------------------------------

In the inifile of your celery service, configure service factories

Sage (default)
...............

.. code-block::

    endi_celery.interfaces.IAccountingFileParser=endi_celery.parsers.sage.parser_factory

.. code-block::

    endi_celery.interfaces.IAccountingOperationProducer=endi_celery.parsers.sage.producer_factory

Sage Generation Expert
.......................

.. code-block::

    endi_celery.interfaces.IAccountingFileParser=endi_celery.parsers.sage_generation_expert.parser_factory

.. code-block::

    endi_celery.interfaces.IAccountingOperationProducer=endi_celery.parsers.sage_generation_expert.producer_factory

Quadra
.......................

.. code-block::

    endi_celery.interfaces.IAccountingFileParser=endi_celery.parsers.quadra.parser_factory

.. code-block::

    endi_celery.interfaces.IAccountingOperationProducer=endi_celery.parsers.quadra.producer_factory
