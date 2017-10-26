from test.udbm import Federation
from symbolic_state.location_vector import LocationVector


class DoubleSymbolicState:

    def __init__(self, location_vector, zone):
        self.location_vector = location_vector
        self.zone = zone

    @staticmethod
    def k_equivalence(k, u1, u2):
        """k is a set of clocks, and
        u1 and u2 is federations and returns if they are equal in the dimensions in k"""
        for clock in k:
            if not (u1.context.hasClockByName(clock) and u2.context.hasClockByName(clock)):
                return False

        # finding the different clocks in u1 and u2
        u1_minus_k = diff(u1, k)
        u2_minus_k = diff(u2, k)

        # freeing the unshared clocks in u1 and k
        for clock in u1_minus_k:
            u1.freeClock(clock)
        # freeing the unshared clocks in u2 and k
        for clock in u2_minus_k:
            u2.freeClock(clock)

        # returning the comparison of the modified u1 and u2
        return u1 == u2


def diff(u1, k):
    """u1 and u2 is a federation, and returns the set differences between u1 and u2's clocks"""
    result = []
    for clock in k:
        if not (u1.context.hasClockByName(clock)):
            result.append(clock)
    return result
