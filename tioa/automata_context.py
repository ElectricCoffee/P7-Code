from symbolic_state.location_vector import LocationVector
from symbolic_state.context_location_vector import ContextLocationVector
from tioa.tioa import TIOA


class AutomataContext(list):
    def __init__(self, automata):
        """Creates an AutomataContext from a list of TIOAs

        Keyword arguments:
        automata -- List of TIOAs

        Assertions:
        All elements of automata are TIOAs
        """
        for automaton in automata:   # TODO: Rewrite this assertion iteration with a helper function.
            assert(isinstance(automaton, TIOA))
        super(AutomataContext, self).__init__(automata)

    def ContextLocationVector(self, locations):
        """Creates a ContextLocationVector with this context

        Keyword arguments:
        locations -- List of locations

        Assertions:
        Each location must be either '*' or included in the corresponding automaton of the context
        """
        _location_vector = ContextLocationVector(self, locations)
        assert(self.is_valid_location_vector(_location_vector))
        return _location_vector

    def is_valid_location_vector(self, location_vector):
        """Checks whether a LocationVector is valid in this context

        Keyword arguments:
        location_vector -- The LocationVector to be checked

        Assertions:
        location_vector is a LocationVector
        """
        assert(isinstance(location_vector, LocationVector))
        for automaton, location in zip(self, location_vector):
            if location != '*' and location not in automaton.locations:
                return False
        return True