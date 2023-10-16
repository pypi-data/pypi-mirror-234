# socketcan-uds

![coverage](https://gitlab.com/Menschel/socketcan-uds/badges/master/coverage.svg)
![pipeline](https://gitlab.com/Menschel/socketcan-uds/badges/master/pipeline.svg)

[Documentation](https://menschel.gitlab.io/socketcan-uds/)

A python 3 implementation of Unified Diagnostic Services (UDS) Protocol specifically targeted for socketcan / linux.

# Description

Goal of this project is to make UDS available in a "pythonic" way, e.g. use built-in types of python3 for efficiency
and "map" the protocol onto the best practices.

# Milestone

All UDS services of 2020's revision are realized in this module.

# Usage

Usage is intended to be simple. UDS is basically a serial port, so use it as one.
You just need to define a CanIsoTpSocket from the corresponding socketcan module and
pass it to the uds constructor.


# License
This software is distributed under GPLv3 with some extension because GPLv3 did not manage to deny
criminal misuse by organizations.
This software is intended for usage by community and private individuals who are interested in car hacking.
It is explicitly denied that any company or organization monetizes on this software. Monetize does not only mean money,
it means gaining a competitive advantage of any kind by using this software.
The author explicitly denies the usage for people associated with military,
government agencies of any kind to whatever degree, same for car manufacturers and associates.