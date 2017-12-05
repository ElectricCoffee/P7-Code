from cbr import *
from dbm.udbm import *
from tioa.tioa import *
from symbolic_state.double_symbolic_state import *
from symbolic_state.location_vector import *
from tioa.automata_context import *
import time


c = Context(['x', 'y'], 'c')

t1 = TIOA(["a1", "b1"], "a1", set(c.clocks),
          [Edge("a1", "a", Guard(c), set(), "b1")], {}, {"a"}, {})
t2 = TIOA(["a2", "b2", "c2"], "a2", set(c.clocks),
          [Edge("a2", "a", Guard(c), set(), "b2"),
           Edge("b2", "b", Guard(c), set(), "c2")], {"a"}, {"b"}, {})
t3 = TIOA(["a3", "b3", "c3"], "a3", set(c.clocks),
          [Edge("a3", "b", Guard(c), set(), "b3"),
           Edge("b3", "c", Guard(c), set(), "c3")], {"b"}, {"c"}, {})
t4 = TIOA(["a4", "b4", "c4"], "a4", set(c.clocks),
          [Edge("a4", "c", Guard(c), set(), "b4"),
           Edge("b4", "d", Guard(c), set(), "c4")], {"c"}, {"d"}, {})
t5 = TIOA(["a5", "b5", "c5"], "a5", set(c.clocks),
          [Edge("a5", "d", Guard(c), set(), "b5"),
           Edge("b5", "e", Guard(c), set(), "c5")], {"d"}, {"e"}, {})
t6 = TIOA(["a6", "b6"], "a6", set(c.clocks),
          [Edge("a6", "e", Guard(c), set(), "b6")], {"e"}, {}, {})

t7 = TIOA(["a7", "b7"], "a7", set(c.clocks),
          [Edge("a7", "a", Guard(c), set(), "b7")], {"a"}, {}, {})

autocon1 = AutomataContext([t1, t2, t3, t4, t5, t6])
autocon2 = AutomataContext([t1, t7, t2, t3, t4, t5])

clocks = set()
for clock_name, clock in c.items():
    clocks.add(clock)

dssinit1 = DoubleSymbolicState(autocon1.ContextLocationVector(["a1", "*", "*", "*", "*", "*"]), c.getTautologyFederation())
dssgoal1 = DoubleSymbolicState(autocon1.ContextLocationVector(["*", "*", "*", "*", "*", "b6"]), c.getTautologyFederation())

#test uden al statespace
dssinit2 = DoubleSymbolicState(autocon2.ContextLocationVector(["a1", "*", "*", "*", "*", "*"]), c.getTautologyFederation())
dssgoal2 = DoubleSymbolicState(autocon2.ContextLocationVector(["*", "b7", "*", "*", "*", "*"]), c.getTautologyFederation())


resfactor = 0
print("How many iterations should the CBR run? ")
nr = int(input())

for x in range(0, nr):
    time_start1 = time.time()
    cbr(dssinit1, dssgoal1, [t1, t2, t3, t4, t5, t6], clocks)
    time_end1 = time.time()

    time_dif1 = (time_end1 - time_start1) * 1000

    time_start2 = time.time()
    cbr(dssinit2, dssgoal2, [t1, t7, t2, t3, t4, t5], clocks)
    time_end2 = time.time()

    time_dif2 = (time_end2 - time_start2) * 1000


    resfactor += time_dif1 / time_dif2
print("Factor between with and without, factor: " + str(resfactor/nr))
