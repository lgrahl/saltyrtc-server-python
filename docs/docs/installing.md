# Installing

**Note:** On machines where Python 3 is not the default Python runtime, you
should use `pip3` instead of `pip`.

## Prerequisites

You need the following packages installed to be able to run the SaltyRTC
server:

- python3
- python3-pip
- libsodium-dev

## Option A: Installing System-Wide

Now install `saltyrtc.server` from [PyPI](https://pypi.python.org/):

    $ sudo pip install saltyrtc.server

## Option B: Installing in a Venv

If you don't want to install saltyrtc-server-python system-wide, we
recommend using [venv](https://docs.python.org/3/library/venv.html) to create
an isolated Python environment.

    $ python3 -m venv venv

You can switch into the created virtual environment venv by running this command:

    $ source venv/bin/activate

While the virtual environment is active, all packages installed using `pip`
will be installed into this environment.

    $ pip install saltyrtc.server
