from symbolic_state.location_vector import LocationVector
from tioa.tioa import TIOA


class ContextLocationVector(LocationVector):
    def __init__(self, context, locations):
        self.context = context
        super(ContextLocationVector, self).__init__(locations)

    def m_equivalence(self, other, m):
        """Checks M_equivalance with another ContextLocationVector

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
