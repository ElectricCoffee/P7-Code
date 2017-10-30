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
        u1_minus_k = diff(u1, k)
        u2_minus_k = diff(u2, k)

        # freeing the unshared clocks in u1 and k
        for clock in u1_minus_k:
            u1 = u1.freeClock(clock)
        # freeing the unshared clocks in u2 and k
        for clock in u2_minus_k:
            u2 = u2.freeClock(clock)

        # returning the comparison of the modified u1 and u2
        return u1 == u2


def diff(u, k):
    """u1 is a federation, and k is a set of clocks and returns the set differences between u1 and k's clocks"""
    result = []
    for clock_name, clock in u.context.items():
        if not (clock_name in k):
            result.append(clock)
    return result
