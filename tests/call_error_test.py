import os
import pickle
import sys

import unittest2

import mitogen.core

import testlib
import plain_old_module


class ConstructorTest(unittest2.TestCase):
    klass = mitogen.core.CallError

    def test_string_noargs(self):
        e = self.klass('%s%s')
        self.assertEquals(e.args[0], '%s%s')

    def test_string_args(self):
        e = self.klass('%s%s', 1, 1)
        self.assertEquals(e.args[0], '11')

    def test_from_exc(self):
        ve = plain_old_module.MyError('eek')
        e = self.klass(ve)
        self.assertEquals(e.type_name, 'plain_old_module.MyError')
        self.assertEquals(e.args[0], 'plain_old_module.MyError: eek')

    def test_form_base_exc(self):
        ve = SystemExit('eek')
        type_name = mitogen.core.qualname(SystemExit)  # varies across 2/3.

        e = self.klass(ve)
        self.assertEquals(e.type_name, type_name)
        self.assertEquals(e.args[0], '%s: eek' % (type_name,))

    def test_from_exc_tb(self):
        try:
            raise plain_old_module.MyError('eek')
        except plain_old_module.MyError:
            ve = sys.exc_info()[1]
            e = self.klass(ve)

        self.assertTrue(e.type_name, 'plain_old_module.MyError')
        self.assertTrue(e.args[0].startswith('plain_old_module.MyError: eek'))
        self.assertTrue('test_from_exc_tb' in e.args[0])


class PickleTest(unittest2.TestCase):
    klass = mitogen.core.CallError

    def test_string_noargs(self):
        e = self.klass('%s%s')
        e2 = pickle.loads(pickle.dumps(e))
        self.assertEquals(e2.type_name, None)
        self.assertEquals(e2.args[0], '%s%s')

    def test_string_args(self):
        e = self.klass('%s%s', 1, 1)
        e2 = pickle.loads(pickle.dumps(e))
        self.assertEquals(e2.type_name, None)
        self.assertEquals(e2.args[0], '11')

    def test_from_exc(self):
        ve = plain_old_module.MyError('eek')
        e = self.klass(ve)
        e2 = pickle.loads(pickle.dumps(e))
        self.assertEquals(e2.type_name, 'plain_old_module.MyError')
        self.assertEquals(e2.args[0], 'plain_old_module.MyError: eek')

    def test_from_exc_tb(self):
        try:
            raise plain_old_module.MyError('eek')
        except plain_old_module.MyError:
            ve = sys.exc_info()[1]
            e = self.klass(ve)

        e2 = pickle.loads(pickle.dumps(e))
        self.assertEquals(e2.type_name, 'plain_old_module.MyError')
        self.assertTrue(e2.args[0].startswith('plain_old_module.MyError: eek'))
        self.assertTrue('test_from_exc_tb' in e2.args[0])


if __name__ == '__main__':
    unittest2.main()
