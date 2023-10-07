# This file is placed in the Public Domain.
#
# pylint: disable=C0114,C0115,C0116,W0703,C0413,R0801
# pylama: ignore=E402


import os
import sys
import unittest


sys.path.insert(0, ".")


from bot.objects import Object
from bot.storage import Storage, sync


from bot import storage


Storage.workdir = '.test'


ATTRS1 = (
          'Storage',
          'fetch',
          'find',
          'fns',
          'sync'
         )


ATTRS1 = [
          'Storage',
          'fetch',
          'find',
          'fns', 
          'read',
          'sync',
          'write'
         ]


class TestStorage(unittest.TestCase):

    def test_constructor(self):
        obj = Storage()
        self.assertTrue(type(obj), Storage)

    def test__class(self):
        obj = Storage()
        clz = obj.__class__()
        self.assertTrue('Storage' in str(type(clz)))

    def test_dirmodule(self):
        self.assertEqual(
                         dir(storage),
                         list(ATTRS1)
                        )

    def test_module(self):
        self.assertTrue(Storage().__module__, 'storage')

    def test_save(self):
        Storage.workdir = '.test'
        obj = Object()
        opath = sync(obj)
        self.assertTrue(os.path.exists(Storage.store(opath)))
