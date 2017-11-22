from symbolic_state.double_symbolic_state import *
from dbm.udbm import *


def cbr(dss_init, dss_goal, m, k):
    """Determind if i t is possible to go from goal to init

    Keyword Arguments:
    dss_init -- the initial Double Symbolic State
    dss_goal -- the goal Double Symbolic State
    m -- An iterable of machines
    k -- An iterable of clocks
    """
    wait = [dss_goal]
    m_new = []
    k_new = []
    for automat in m:
        m_new.append(automat)
        for clock in k:
            k_new.append(clock)
            passed = []
            for symbolicstate in wait:
                if symbolicstate == dss_init:
                    return True
                else:
                    for symbolicstate_new in passed:
                        if not symbolicstate <= symbolicstate_new:
                            passed.append(symbolicstate)
                            next = symbolicstate.mk_predecessors(m_new, k_new)
                            for j in next:
                                wait.append(j)
            for x in passed:
                wait.append(x)
    return False
