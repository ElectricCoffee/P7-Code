import sys
sys.path.insert(0, '../test/')
from udbm import *
sys.path.insert(0, '../symbolic_state/')
from location_vector import *


class DoubleSymbolicState:

    def __init__(self, location_vector, zone):
        self.location_vector = location_vector
        self.zone = zone

    def k_equivalence(self, other, k):
        """k is a set of clocks, and
        u1 and u2 is federations and returns if they are equal in the dimensions in k"""

        u1 = self.zone
        u2 = other.zone

        for clock in k:
            if not u1.context.hasClockByName(clock):
                return False
            elif not u2.context.hasClockByName(clock):
                return False

        # finding the different clocks in u1 and u2
        u1_minus_k = _diff(u1, k)
        u2_minus_k = _diff(u2, k)

        # freeing the unshared clocks in u1 and k
        for clock in u1_minus_k:
            u1.freeClock(clock)
        # freeing the unshared clocks in u2 and k
        for clock in u2_minus_k:
            u2.freeClock(clock)

        # returning the comparison of the modified u1 and u2
        return u1 == u2

    def _diff(self, k):
        """u1 and u2 is a federation, and returns the set differences between u1 and u2's clocks"""
        result = []
        for clock in k:
            if not (self.zone.context.hasClockByName(clock)):
                result.append(clock)
        return result
