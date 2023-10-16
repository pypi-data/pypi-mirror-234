from unittest import TestCase


class BaseTestCase(TestCase):
    """
    Root test class with defaults for all tests.
    """

    @classmethod
    def setUpClass(cls):
        TestCase.setUpClass()

    @classmethod
    def tearDownClass(cls):
        TestCase.tearDownClass()

    def setUp(self):
        super().setUp()
        self.maxDiff = None

    def tearDown(self):
        super().tearDown()
