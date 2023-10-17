openmairie.robotframework
=========================

RobotFramework Library for functional testing openMairie Framework based apps

.. image:: https://img.shields.io/pypi/v/openmairie.robotframework.svg
    :target: https://pypi.python.org/pypi/openmairie.robotframework/
    :alt: Latest PyPI version

.. contents::

Introduction
------------

openmairie.robotframework is a  `RobotFramework <http://robotframework.org/>`_
library who provide keywords to `openMairie Framework <http://www.openmairie.org/framework/>`_
based projects.


Installation
------------

You just need `pip <https://pip.pypa.io>`_ ::

    pip install openmairie.robotframework


Due to the history of this package all the keywords are declared in .robot
files. So you need to call the Reload Library in each Suite Setup. ::

    *** Settings ***
    Library  openmairie.robotframework.Library

    *** Keywords ***
    For Suite Setup
        Reload Library  openmairie.robotframework.Library


Keywords Documentation
----------------------

- https://openmairie.gitlab.io/openmairie.robotframework/

