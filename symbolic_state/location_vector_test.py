import unittest
from location_vector import *


class LocationVectorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.p = LocationVector([1, 2])
        cls.q = LocationVector([1, '*'])
        cls.r = LocationVector(['*', 1])

    def test_strictIn(self):
        self.assertFalse(p < p)
        self.assertTrue(p < q)
        self.assertFalse(p < r)
        self.assertFalse(q < p)
        self.assertFalse(q < q)
        self.assertFalse(q < r)
        self.assertFalse(r < p)
        self.assertFalse(r < q)
        self.assertFalse(r < r)

    def test_in(self):
        self.assertTrue(p <= p)
        self.assertTrue(p <= q)
        self.assertFalse(p <= r)
        self.assertFalse(q <= p)
        self.assertTrue(q <= q)
        self.assertFalse(q <= r)
        self.assertFalse(r <= p)
        self.assertFalse(r <= q)
        self.assertTrue(r <= r)

    def test_revstrictin(self):
        self.assertFalse(p > p)
        self.assertFalse(p > q)
        self.assertFalse(p > r)
        self.assertTrue(q > p)
        self.assertFalse(q > q)
        self.assertFalse(q > r)
        self.assertFalse(r > p)
        self.assertFalse(r > q)
        self.assertFalse(r > r)

    def test_revin(self):
        self.assertTrue(p >= p)
        self.assertFalse(p >= q)
        self.assertFalse(p >= r)
        self.assertTrue(q >= p)
        self.assertTrue(q >= q)
        self.assertFalse(q >= r)
        self.assertFalse(r >= p)
        self.assertFalse(r >= q)
        self.assertTrue(r >= r)

if __name__ == '__main__':
    unittest.main()