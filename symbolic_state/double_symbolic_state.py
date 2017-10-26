from test.udbm import Federation
from symbolic_state.location_vector import LocationVector


class DoubleSymbolicState:

    def __init__(self, location_vector, zone):
        self.location_vector = location_vector
        self.zone = zone

    @staticmethod
    def k_equivalence(k, zone, other_zone):
        pass
