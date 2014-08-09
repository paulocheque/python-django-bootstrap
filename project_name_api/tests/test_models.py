import unittest
from django_dynamic_fixture import G, F


class XTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_x(self):
        a = G(Account)
        p = a.current_plan()
        self.assertEquals(p.plan_type, '1')