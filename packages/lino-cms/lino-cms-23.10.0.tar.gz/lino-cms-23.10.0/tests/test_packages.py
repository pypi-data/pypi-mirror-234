# python setup.py test -s tests/test_packages.py

from lino_cms import SETUP_INFO
from lino.utils.pythontest import TestCase

class PackagesTests(TestCase):

    def test_packages(self):
        self.run_packages_test(SETUP_INFO['packages'])
