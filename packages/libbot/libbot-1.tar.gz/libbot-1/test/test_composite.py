# This file is placed in the Public Domain.
#
# pylint: disable=W0611,C0114,C0115,C0116,C0413,E1101,R1732
# pylama: ignore=E265,E402


import unittest


from bot.objects import Object
from bot.storage import Storage, fetch, sync


Storage.workdir = ".test"


class TestComposite(unittest.TestCase):

    def testcomposite(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.a = "test"
        self.assertEqual(obj.obj.a, "test")

    def testcompositeprint(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.a = "test"
        sync(obj)
        ooo = Object()
        fetch(ooo, obj.__fnm__)
        self.assertTrue(ooo.obj)
