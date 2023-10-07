# This file is placed in the Public Domain.
#
# pylint: disable=W0406,C0413
# flake8: noqa


"modules"


import os
import sys


from . import cmd, irc, log, mod, rss, sts, tdo, thr


def __dir__():
    return (
            'cmd',
            'irc',
            'log',
            'mod',
            'rss',
            'sts',
            'tdo',
            'thr'
           )
