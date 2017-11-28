from symbolic_state.double_symbolic_state import *
from dbm.udbm import *
from operator import and_


def cbr(dss_init, dss_goal, m, k):
    """Determind if i t is possible to go from goal to init

    Keyword Arguments:
    dss_init -- the initial Double Symbolic State
    dss_goal -- the goal Double Symbolic State
    m -- An iterable of machines
    k -- An iterable of clocks
    """
    wait = {dss_goal}
    m_new = set()
    k_new = set()
    for automat in m:
        m_new.add(automat)
        for clock in k:
            k_new.add(clock)
            passed = set()
            while len(wait) != 0:
                symbolicstate = wait.pop()
                if symbolicstate.intersects(dss_init):
                    return True
                else:
                    if len(passed) == 0 or reduce(and_, map(lambda state: not symbolicstate <= state, passed)):
                        passed.add(symbolicstate)
                        next = symbolicstate.mk_predecessors(m_new, k_new)
                        for j in next:
                            wait.add(j)
            wait = passed
    return False
