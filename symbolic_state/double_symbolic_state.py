from dbm.udbm import Federation

class DoubleSymbolicState:
    def __init__(self, location_vector, zone):
        self.location_vector = location_vector
        self.zone = zone

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
        predecessors = []

        for option in self._get_predecessor_options(m, k):
            predecessors += self._predecessor_from_option(option)
        return predecessors

    def _get_predecessor_options(self, m, k):
        optionsbyaction = {}
        actions = set(map(lambda auto: auto.input_actions + auto.output_actions, m))
        for a in actions:
            optionsbyaction[a] = {}

        for location, automaton in filter(lambda (l, a): a in m,
                                          zip(self.location_vector, self.location_vector.context)):
            for a in actions:
                def is_valid_edge(edge):
                    return edge.action == a and edge.guard.k_sorted(k)

                edges = filter(is_valid_edge, automaton.preceeding_edges[location])
                if edges == []:
                    if a in automaton.input_actions + automaton.output_actions:
                        del optionsbyaction[a]
                else:
                    optionsbyaction[a][automaton] = edges
            actions = optionsbyaction.keys()

        for a in optionsbyaction.keys():
            for option in DoubleSymbolicState._generate_options(optionsbyaction[a], 0):
                yield option

    @staticmethod
    def _generate_options(options, k):
        if len(options) == k:
            yield {}
        else:
            automaton, edges = options.items()[k]
            for edge in edges:
                for option in DoubleSymbolicState._generate_options(options, k + 1):
                    option[automaton] = edge
                    yield option

    def _predecessor_from_option(self, option):
        beforeinvariant = self.zone.context.getTautologyFederation()
        afterinvariant = self.zone.context.getTautologyFederation()
        guard = self.zone.context.getTautologyFederation()
        resetzone = self.zone.context.getTautologyFederation()
        reset = {}
        newlocations = []

        for location, automaton in zip(self.location_vector, self.location_vector.context):
            edge = option[automaton]
            if edge is None:
                newlocations += location
            else:
                newlocations += edge.initial_location
        newlocationvector = self.location_vector.context.ContextLocationVector(newlocations)
        for edge in option.values():
            guard &= edge.guard
            reset |= edge.reset
        for clock in reset:
            resetzone.resetValueInPlace(clock)
        for location, automaton in zip(self.location_vector, self.location_vector.context):
            if location != '*':
                afterinvariant &= automaton.invariants[location]
        for location, automaton in zip(newlocationvector, self.location_vector.context):
            if location != '*':
                beforeinvariant &= automaton.invariants[location]

        newzone = DoubleSymbolicState._freeclocks(reset, self.zone.down & afterinvariant & resetzone) & guard & beforeinvariant
        return DoubleSymbolicState(newlocationvector, newzone)

    @staticmethod
    def _freeclocks(clocks, zone):
        for clock in clocks:
            zone.freeClockInPlace(clock)

def diff(u, k):
    """finds the differences between u and k

    Keyword arguments:
    u -- is a federation
    k -- is a set of clocknames
    """
    result = []
    for clock_name, clock in u.context.items():
        if not (clock_name in k):
            result.append(clock)
    return result