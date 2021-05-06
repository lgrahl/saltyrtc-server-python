SaltyRTC Signalling Server
==========================

|CircleCI| |codecov| |PyPI| |Gitter|

This is a SaltyRTC server implementation for Python 3.6 or 3.7 using
`asyncio`_. (Note that currently Python 3.8+ is not supported! We recommend
using Python 3.7.)

Note
****

On machines where Python 3 is not the default Python runtime, you should
use ``pip3`` instead of ``pip``.

Prerequisites
*************

.. code-block:: bash

    sudo apt-get install python3 python3-pip
    
    pip install logbook
    

Mac
***

.. code-block:: bash

    brew install libsodium

We recommend using `venv`_ to create an isolated Python environment:

.. code-block:: bash

    pyvenv venv

You can switch into the created virtual environment *venv* by running
this command:

.. code-block:: bash

    source venv/bin/activate

While the virtual environment is active, all packages installed using
``pip`` will be installed into this environment.

To deactivate the virtual environment, just run:

.. code-block:: bash

    deactivate

If you want easier handling of your virtualenvs, you might also want to
take a look at `virtualenvwrapper`_.

Installation
************

If you are using a virtual environment, activate it first.

Install the module by running:

.. code-block:: bash

    pip install saltyrtc.server

The dependency ``libnacl`` will be installed automatically. However, you
may need to install `libsodium`_ for ``libnacl`` to work.

Command Line Usage
******************

The script ``saltyrtc-server`` will be automatically installed and
provides a command line interface for the server.

Run the following command to see detailed usage information:

.. code-block:: bash

    saltyrtc-server --help

All command line options are also available as environment variables by
prefixing them with `SALTYRTC_SERVER_` and the upper case command name,
followed by the option name in upper case. For example:
`SALTYRTC_SERVER_SERVE_PORT=8765`.

Quick Start
-----------

Generate a new *private permanent key*:

.. code-block:: bash

    saltyrtc-server generate /path/to/permanent-key

Run the following command to start the server on any address with port `8765`:

.. code-block:: bash

    saltyrtc-server serve \
        -p 8765 \
        -tc /path/to/x509-certificate \
        -tk /path/to/key \
        -k /path/to/permanent-key

Alternatively, provide the options via environment variables:

.. code-block:: bash

    export SALTYRTC_SERVER_SERVE_PORT=8765 \
           SALTYRTC_SERVER_SERVE_TLSCERT=/path/to/x509-certificate \
           SALTYRTC_SERVER_SERVE_TLSKEY=/path/to/key \
           SALTYRTC_SERVER_SERVE_KEY=/path/to/permanent-key
    saltyrtc-server serve

Docker
------

You can also use our `official Docker images`_ to run the server:

.. code-block:: bash

    docker run \
        -v /path/to/cert-and-keys:/var/saltyrtc \
        -p 8765:8765
        -it saltyrtc/saltyrtc-server-python:<tag> serve \
        -p 8765 \
        -tc /var/saltyrtc/x509-certificate \
        -tk /var/saltyrtc/key \
        -k /var/saltyrtc/permanent-key

The above command maps port `8765` of the server within the container to port
`8765` on the host machine.

Of course it is also possible to use environment variables to provide the
options, as explained in the previous section.

Contributing
************

If you want to contribute to this project, you should install the
optional ``dev`` requirements of the project in an editable environment:

.. code-block:: bash

    git clone https://github.com/saltyrtc/saltyrtc-server-python.git
    cd saltyrtc-server-python
    pip install -e .[dev]

Before creating a pull request, it is recommended to run the following
commands to check for code style violations (``flake8``), optimise
imports (``isort``), do a static type analysis and run the project's tests:

.. code-block:: bash

    flake8 .
    isort .
    MYPYPATH=${PWD}/stubs mypy saltyrtc examples
    py.test

Reporting Security Issues
*************************

Please report security issues directly to one or both of the following
contacts:

-  Danilo Bargen

   -  Email: mail@dbrgn.ch
   -  Threema: EBEP4UCA
   -  GPG: `EA456E8BAF0109429583EED83578F667F2F3A5FA`_

-  Lennart Grahl

   -  Email: lennart.grahl@gmail.com
   -  Threema: MSFVEW6C
   -  GPG: `3FDB14868A2B36D638F3C495F98FBED10482ABA6`_

.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _venv: https://docs.python.org/3/library/venv.html
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/
.. _libsodium: https://download.libsodium.org/doc/installation/
.. _official Docker images: https://hub.docker.com/r/saltyrtc/saltyrtc-server-python

.. |CircleCI| image:: https://circleci.com/gh/saltyrtc/saltyrtc-server-python.svg?style=shield
   :target: https://circleci.com/gh/saltyrtc/saltyrtc-server-python
.. |codecov| image:: https://codecov.io/gh/saltyrtc/saltyrtc-server-python/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/saltyrtc/saltyrtc-server-python
.. |PyPI| image:: https://badge.fury.io/py/saltyrtc.server.svg
   :target: https://badge.fury.io/py/saltyrtc.server
.. |Gitter| image:: https://badges.gitter.im/saltyrtc/Lobby.svg
   :target: https://gitter.im/saltyrtc/Lobby
.. _EA456E8BAF0109429583EED83578F667F2F3A5FA: https://keybase.io/dbrgn
.. _3FDB14868A2B36D638F3C495F98FBED10482ABA6: https://keybase.io/lgrahl
