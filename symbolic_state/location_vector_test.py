import unittest
from location_vector import *

class LocationVectorTest(unittest.TestCase):
    p = LocationVector([1, 2])
    q = LocationVector([1, '*'])
    r = LocationVector(['*', 1])

    def StrictIn(self):
        self.assertFalse(self.p < self.p)
        self.assertTrue(self.p < self.q)
        self.assertFalse(self.p < self.r)
        self.assertFalse(self.q < self.p)
        self.assertFalse(self.q < self.q)
        self.assertFalse(self.q < self.r)
        self.assertFalse(self.r < self.p)
        self.assertFalse(self.r < self.q)
        self.assertFalse(self.r < self.r)

    def In(self):
        self.assertTrue(self.p <= self.p)
        self.assertTrue(self.p <= self.q)
        self.assertFalse(self.p <= self.r)
        self.assertFalse(self.q <= self.p)
        self.assertTrue(self.q <= self.q)
        self.assertFalse(self.q <= self.r)
        self.assertFalse(self.r <= self.p)
        self.assertFalse(self.r <= self.q)
        self.assertTrue(self.r <= self.r)

    def RevStrictIn(self):
        self.assertFalse(self.p > self.p)
        self.assertFalse(self.p > self.q)
        self.assertFalse(self.p > self.r)
        self.assertTrue(self.q > self.p)
        self.assertFalse(self.q > self.q)
        self.assertFalse(self.q > self.r)
        self.assertFalse(self.r > self.p)
        self.assertFalse(self.r > self.q)
        self.assertFalse(self.r > self.r)

    def RevIn(self):
        self.assertTrue(self.p >= self.p)
        self.assertFalse(self.p >= self.q)
        self.assertFalse(self.p >= self.r)
        self.assertTrue(self.q >= self.p)
        self.assertTrue(self.q >= self.q)
        self.assertFalse(self.q >= self.r)
        self.assertFalse(self.r >= self.p)
        self.assertFalse(self.r >= self.q)
        self.assertTrue(self.r >= self.r)

if __name__ == '__main__':
    unittest.main()