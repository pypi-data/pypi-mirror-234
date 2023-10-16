"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_debts
  $ python setup.py test -s tests.DocsTests.test_docs
"""
from unipath import Path

ROOTDIR = Path(__file__).parent.parent

SETUP_INFO = {}

# load SETUP_INFO:
filename = ROOTDIR.child('lino_cms', 'setup_info.py')
exec(compile(open(filename, "rb").read(), filename, 'exec'))

from lino.utils.pythontest import TestCase

import os
#os.environ['DJANGO_SETTINGS_MODULE'] = "lino_cms.settings.test"


# class BaseTestCase(TestCase):
#     project_root = ROOTDIR
#     django_settings_module = 'lino_noi.settings.test'


class PackagesTests(TestCase):

    def test_packages(self):
        self.run_packages_test(SETUP_INFO['packages'])


class SpecsTests(TestCase):

    def test_general(self):
        self.run_simple_doctests('docs/specs/general.rst')

    def test_db(self):
        self.run_simple_doctests('docs/specs/db.rst')

    def test_roles(self):
        self.run_simple_doctests('docs/specs/roles.rst')


class DemoTests(TestCase):
    """Run tests on the demo projects.
    """

    def test_cms(self):
        self.run_django_manage_test('lino_cms/projects/cms')

