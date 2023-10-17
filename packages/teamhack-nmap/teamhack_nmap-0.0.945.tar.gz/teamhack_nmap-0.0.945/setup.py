#! /usr/bin/env python
from os         import environ
from setuptools import setup

if __name__ == '__main__':
  setup(version=environ.get("TEAMHACK_VERSION"))

