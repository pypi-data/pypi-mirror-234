# This file is placed in the Public Domain.
#
# pylint: disable=C0112,C0115,C0116,W0105,R0903,E0402,C0209,R1710


"storage"


import inspect
import os
import time


from .methods import fqn, ident, search
from .objects import Object, read, update, write
from .utility import cdir, strip


def  __dir__():
    return (
            'Storage',
            'fetch',
            'find',
            'fns',
            'read',
            'sync',
            'write'
           )


class Storage:

    classes = {}
    workdir = ""

    @staticmethod
    def add(clz):
        if not clz:
            return
        name = str(clz).split()[1][1:-2]
        Storage.classes[name] = clz

    @staticmethod
    def files() -> []:
        return os.listdir(Storage.store())

    @staticmethod
    def long(name):
        split = name.split(".")[-1].lower()
        res = name
        for named in Storage.classes:
            if split in named.split(".")[-1].lower():
                res = named
                break
        return res

    @staticmethod
    def path(pth):
        if not pth:
            pth = ""
        pth2 =  os.path.join(Storage.workdir, pth)
        cdir(pth2)
        return pth2

    @staticmethod
    def store(pth=""):
        pth = os.path.join(Storage.workdir, "store", pth)
        cdir(pth)
        return pth

    @staticmethod
    def scan(mod) -> None:
        for key, clz in inspect.getmembers(mod, inspect.isclass):
            if key.startswith("cb"):
                continue
            if not issubclass(clz, Object):
                continue
            Storage.add(clz)


def find(mtc, selector=None) -> []:
    if selector is None:
        selector = {}
    clz = Storage.long(mtc)
    for fnm in reversed(sorted(fns(clz), key=fntime)):
        obj = Object()
        fetch(obj, fnm)
        if '__deleted__' in obj:
            continue
        if selector and not search(obj, selector):
            continue
        yield obj


def fns(mtc) -> []:
    dname = ''
    pth = Storage.store(mtc)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            dname = sorted(dirs)[-1]
            if dname.count('-') == 2:
                ddd = os.path.join(rootdir, dname)
                fls = sorted(os.listdir(ddd))
                if fls:
                    yield strip(os.path.join(ddd, fls[-1]))


def fntime(daystr) -> float:
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    else:
        timed = 0
    return timed


def fetch(obj, pth):
    pth2 = Storage.store(pth)
    read(obj, pth2)
    obj.__fnm__ = strip(pth)


def last(obj, selector=None) -> None:
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x.__fnm__)
                   )
    if result:
        inp = result[-1]
        update(obj, inp)
        obj.__fnm__ = inp.__fnm__


def sync(obj, pth=None):
    pth = pth or obj.__fnm__
    if not pth:
        pth = ident(obj)
    pth2 = Storage.store(pth)
    write(obj, pth2)
    obj.__fnm__ = pth
    return pth
