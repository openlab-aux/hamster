# hamster

A frontend for the [lsmsd](https://github.com/openlab-aux/lsmsd)
backend. Written in python with qt. It is used to manage the inventory
for our local hackerspace.

# Prerequisites

Hamster is written for python 2 and 3. The following libraries are
needed:

- [requests](http://docs.python-requests.org/en/latest/)
- [pyqt4](http://pyqt.sourceforge.net/Docs/PyQt4/) or [pyside](https://wiki.qt.io/PySideDocumentation)

On debian bases systems:

```bash
apt-get install python3-request python3-pyside
```

Or with easy_install/pip

```bash
pip install PySide requests
```

# Name

Since hamsters can store a lot of food in their spacious cheek pouches
and this software (together with [lsmsd](https://github.com/openlab-aux/lsmsd))
is used to manage storage, it is named hamster.
