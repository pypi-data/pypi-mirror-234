# This file is placed in the Public Domain.
#
# pylint: disable=C0114,C0115,C0116,W0703,C0413
# pylama: ignore=E402


import unittest


from bot.objects  import Object, dumps


VALIDJSON = '{"test": "bla"}'


class TestEncoder(unittest.TestCase):

    def test_dumps(self):
        obj = Object()
        obj.test = "bla"
        self.assertEqual(dumps(obj), VALIDJSON)
