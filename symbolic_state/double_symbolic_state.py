from dbm.udbm import Federation
from operator import or_

class DoubleSymbolicState:
    def __init__(self, location_vector, zone):
        self.location_vector = location_vector
        self.zone = zone

    def __eq__(self, other):
        return self.mk_equivalence(other, self.zone.context.clocks, self.location_vector.context)

    def __hash__(self):
        return hash(hash(self.location_vector) + hash(self.zone))

    def k_equivalence(self, other, k):
        """Determind if self and other is k-equivalent

        Keyword arguments:
        other -- is a double symbolic state
        k  -- is a set of clocknames
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

    def mk_equivalence(self, other, k, m):
        """determind if self and other are mk-equivalent

        Keyword arguments:
            other -- is a double symbolic state
            k -- is a set of clocknames
            m -- is a set of automata, where locations must be equal
        """
        return (self.k_equivalence(other, k)) and \
            (self.location_vector.m_equivalence(other.location_vector, m))

    def mk_predecessors(self, m, k):
        """Finds the symbolic mk predecessors of this state given the context of its constituents

        Keyword arguments:
        m -- An iterable of machines
        k -- An iterable of clocks

        Assertions:
        m is in the context of the location vector of self
        k is in the context of the zone of self
        """
        for automaton in m:
            assert(automaton in self.location_vector.context)
        for clock in k:
            assert(self.zone.context is clock.context)

        predecessors = []

        # For all possible options
        for option in self._get_predecessor_options(m, k):
            # Find the resulting predecessor
            predecessor = self._predecessor_from_option(option)
            # Only consider the predecessor if it has a non-empty zone
            if not predecessor.zone.isEmpty():
                predecessors.append(predecessor)
        return predecessors

    def _get_predecessor_options(self, m, k):
        """Calculates all possible options for precedence given mk

        Keyword arguments:
        m -- An iterable of machines
        k -- An iterable of clocks
        """
        # Store all actions known to m as a set
        actions = reduce(or_, map(lambda auto: auto.input_actions | auto.output_actions, m))

        # Remove all actions known outside of m
        for automaton in self.location_vector.context:
            if automaton not in m:
                actions -= automaton.input_actions | automaton.output_actions

        optionsbyaction = {}
        # The resulting options will be grouped by action
        for a in actions:
            optionsbyaction[a] = {}

        # For all locations, automata from self.location_vector that are in m
        for location, automaton in filter(lambda (_, auto): auto in m,
                                          zip(self.location_vector, self.location_vector.context)):
            invalidactions = set()
            for a in actions:
                # Predicate tests if edge can be followed with the action a
                def is_valid_edge(edge):
                    return edge.action == a and edge.guard.k_sorted(k)
                # Find all preceding edges that can be followed with the action a
                edges = filter(is_valid_edge, automaton.preceeding_edges[location])
                if edges == []:
                    # If there are no such edges and the automaton knows of the action a,
                    if a in automaton.input_actions | automaton.output_actions:
                        # then the action a cannot be taken since no possible N can exist.
                        invalidactions.add(a)
                    # Else the action could still be valid, but this automaton is not in N. Nothing should be done.
                # If there are such edges
                else:
                    # Then this automaton is in N and the edges should be considered as options.
                    optionsbyaction[a][automaton] = edges
            # Update actions to remove the invalid actions.
            # This cannot be done while iterating over it.
            actions -= invalidactions

        # Finally _generate_options is called to get all permutations of edges that could be chosen
        for a in actions:
            for option in DoubleSymbolicState._generate_options(optionsbyaction[a]):
                yield option

    @staticmethod
    def _generate_options(options, k = 0):
        """Generates all permutations of edges that can be chosen

        Keyword arguments:
        options -- A dictionary of edges grouped by automaton
        k -- An integer used for recursion.
        """
        if len(options) == 0:
            yield {}
        elif len(options) == k + 1:
            automaton, edges = options.items()[k]
            for edge in edges:
                yield {automaton:edge}
        else:
            automaton, edges = options.items()[k]
            for edge in edges:
                for option in DoubleSymbolicState._generate_options(options, k + 1):
                    option[automaton] = edge
                    yield option

    def _predecessor_from_option(self, option):
        """Calculates the predecessor caused from a given option

        Keyword arguments:
        option -- A dictionary that maps an automaton to its transition edge, if it is in N.
        """

        # Initialize unrestricted zones for accumulation.
        beforeinvariant = self.zone.context.getTautologyFederation()
        afterinvariant = self.zone.context.getTautologyFederation()
        guard = self.zone.context.getTautologyFederation()
        resetzone = self.zone.context.getTautologyFederation()
        reset = set()
        newlocations = []

        # For all automata
        for location, automaton in zip(self.location_vector, self.location_vector.context):
            edge = option.get(automaton)
            # If the automaton is not in N
            if edge is None:
                # The location remains the same
                newlocations.append(location)
            # Otherwise
            else:
                #The new location is the initial location of the edge from option
                newlocations.append(edge.initial_location)
        # Initialize the resulting location vector with the new locations
        newlocationvector = self.location_vector.context.ContextLocationVector(newlocations)

        # Accumulate the guards and resets of the edges from option
        for edge in option.values():
            guard &= edge.guard.zone
            reset |= edge.reset
        # Calculate the resetzone by reseting all reset clocks in an unrestricted zone
        for clock in reset:
            resetzone.resetValueInPlace(clock)
        # Accumulate the invariants of the locations before the transition
        for location, automaton in zip(self.location_vector, self.location_vector.context):
            # Only concrete locations are considered
            if location != '*':
                invariant = automaton.invariants.get(location)
                if invariant is not None:
                    afterinvariant &= invariant
        # Accumulate the invariants of the locations after the transition
        for location, automaton in zip(newlocationvector, self.location_vector.context):
            # Only concrete locations are considered
            if location != '*':
                invariant = automaton.invariants.get(location)
                if invariant is not None:
                    beforeinvariant &= invariant

        # Calculate the new zone
        newzone = DoubleSymbolicState._freeclocks(reset, self.zone.down() & afterinvariant & resetzone) & guard & beforeinvariant
        # Initialize the resulting state and return it
        return DoubleSymbolicState(newlocationvector, newzone)

    @staticmethod
    def _freeclocks(clocks, zone):
        newzone = zone.copy()
        for clock in clocks:
            newzone.freeClockInPlace(clock)
        return newzone

    def __le__(self, other):
        return self.zone <= other.zone and self.location_vector <= other.locationvector


def diff(u, k):
    """finds the differences between u and k

    Keyword arguments:
    u -- is a federation
    k -- is a set of clocknames
    """
    result = []
    k_names = map(lambda clk: clk.name, k)
    for clock_name, clock in u.context.items():
        if not (clock_name in k_names):
            result.append(clock)
    return result