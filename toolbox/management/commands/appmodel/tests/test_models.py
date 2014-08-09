import unittest
from nose.tools import raises

from django.test import TestCase
from django.contrib.auth.models import User

from django_dynamic_fixture import G, F, P


class SampleTests(unittest.TestCase):
    def test_1(self):
        self.assertEquals(True, True)


class SampleTests2(TestCase):
    def test_2(self):
        user = G(User)
        self.assertEquals(user in User.objects.all())

    @raises(Exception)
    def test_3(self):
        raise Exception()