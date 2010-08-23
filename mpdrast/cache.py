# -*- coding: utf-8 -*-

import pickle
from os.path import join, expanduser, exists, getmtime, isdir
from os import makedirs
from hashlib import sha1

USER_DIR = join(expanduser('~'), '.mpdrast')

def cache(name):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            _updated = kwargs["_updated"]
            del kwargs["_updated"]

            if kwargs.has_key("_hash"):
                _hash = kwargs["_hash"]
                del kwargs["_hash"]
            else:
                _hash = uhash()

            cache_dir = join(USER_DIR, "cache", name)
            if not isdir(cache_dir):
                makedirs(cache_dir)

            cache_file = join(cache_dir, _hash)
            if not exists(cache_file) or \
                getmtime(cache_file) < _updated:
                data = fn(*args, **kwargs)
                with open(cache_file, 'w') as handle:
                    pickle.dump(data, handle)
            else:
                with open(cache_file, 'r') as handle:
                    data = pickle.load(handle)

            return data

        return wrapper

    return decorator

def uhash(*args):
    return sha1(pickle.dumps(args)).hexdigest()

def test():
    from tempfile import mkdtemp
    from time import time

    # TODO we should clean up after, also… it's kinda ugly
    globals()["USER_DIR"] = mkdtemp(prefix='mpdrast')
    print "Testing in %s." % USER_DIR

    we_should_be_here = False
    testval = "plop"

    @cache("test")
    def f1():
        assert we_should_be_here
        return testval

    @cache("test2")
    def f2(testparam):
        assert we_should_be_here
        return testparam

    # Handling of the updated parameter
    we_should_be_here = True
    assert "plop" == f1(_updated=1)
    we_should_be_here = False
    testval = "plop2"
    assert "plop" == f1(_updated=1)
    we_should_be_here = True
    assert "plop2" == f1(_updated=time()+42)

    # Different cache for different parameters
    we_should_be_here = True
    assert "plap" == f2(_updated=1, _hash=uhash("plap"), testparam="plap")
    we_should_be_here = False
    assert "plap" == f2(_updated=1, _hash=uhash("plap"), testparam="plap")
    we_should_be_here = True
    assert "plip" == f2(_updated=1, _hash=uhash("plip"), testparam="plip")

