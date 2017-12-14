from .location_vector import LocationVector
from tioa.tioa import TIOA


class ContextLocationVector(LocationVector):
    def __init__(self, context, locations):
        self.context = context
        super(ContextLocationVector, self).__init__(locations)

    @staticmethod
    def static_m_equivalence(location_vector, other_location_vector, m):
        """Checks M_equivalence between two ContextLocationVectors ContextLocationVector
        
        Keyword arguments:
        location_vector -- The first ContextLocationVector in the comparison
        other_location_vector -- The other ContextLocationVector in the comparison
        m -- The set of automata, where locations must be equal

        Assertions:
        None
        """

        return location_vector.m_equivalence(other_location_vector, m)

    def m_equivalence(self, other, m):
        """Checks M_equivalence with another ContextLocationVector

        Keyword arguments:
        other -- Another ContextLocationVector be be compared with
        m -- The set of automata, where locations must be equal

        Assertions:
        other is a ContextLocationVector
        self and other share the same context
        All elements of m are TIOAs
        """
        assert(isinstance(other, ContextLocationVector))
        assert(self.context == other.context)
        for automaton in m:   # TODO: Rewrite this assertion iteration with a helper function.
            assert(isinstance(automaton, TIOA))

        for automaton, location, other_location in zip(self.context, self, other):
            if automaton in m and location != other_location:
                return False
        return True