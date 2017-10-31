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
        """Determind if self and other is k-equivalent

        Keyword arguments:
            --other is a double symbolic state
            --k is a set of clocknames
        """
        # u1 and u2 is a federation
        u1 = self.zone
        u2 = other.zone

        if u1.context.clocks != u2.context.clocks:
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
    """finds the differences between u and k

    Keyword arguments:
        --u is a federation
        --k is a set of clocknames
    """
    result = []
    for clock_name, clock in u.context.items():
        if not (clock_name in k):
            result.append(clock)
    return result
