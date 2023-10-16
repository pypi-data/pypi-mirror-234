#! /usr/bin/env python

from setuptools import Command, Extension, setup, find_packages
from setuptools.command.build_ext import build_ext


DISTNAME = "robo-utils"
#DESCRIPTION = "robo utils "

#mk  works
import roboutils


if __name__ == "__main__":
    setup()
